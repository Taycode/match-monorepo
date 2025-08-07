import json
import logging
import math
from typing import List, Dict, Any, Tuple
from django.conf import settings
import hashlib
from tweepy import Client
from openai_client.client import OpenAPIClient
from postings.models import Job, FormResponse, Match
from talents.models import Talent
from vector.service import VectorManager
from postings.google_services import (
    create_google_form as create_form,
    create_google_sheet as create_sheet,
    grant_form_permissions,
    get_sheet_responses
)
from openai_client.schemas.job_schema import JOB_PARSER_SCHEMA
from common.utils.document_reader import DocumentReader
from talents.service import parse_candidate_resume
from django.core.cache import cache

logger = logging.getLogger(__name__)


def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    """
    if len(vector1) != len(vector2):
        logger.warning(
            f"Vector length mismatch: {len(vector1)} vs {len(vector2)}")
        return 0.0

    # Handle zero vectors
    if not any(vector1) or not any(vector2):
        return 0.0

    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vector1, vector2))

    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Calculate cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)

    # Clamp to [-1, 1] range and convert to [0, 1] range
    similarity = max(-1.0, min(1.0, similarity))
    similarity = (similarity + 1.0) / 2.0  # Convert from [-1,1] to [0,1]

    return similarity


def get_structured_data_for_job(job_title: str, job_description: str) -> Dict[str, str | int | float | List[str]]:
    if not job_description.strip():
        logger.warning(
            "Empty job description provided for structured data extraction")
        return {}
    try:
        # Use OpenAI to extract structured job data
        logger.info("Extracting structured job data using OpenAI")
        response = OpenAPIClient.query_for_json(
            "You are an expert at structured data extraction. "
            "You will be given unstructured job title and description text from a "
            "job posting and should convert it into the given structure."
            "Not applicable fields can be set to null."
            "Ensure the role field is a specific job title or " \
            "role the job is targeting? Return a list of likely role names"
            "Ensure the extracted data is relevant to "
            "or inferred from  the job posting.",
            f"{job_title}\n{job_description}",
            JOB_PARSER_SCHEMA
        )
        json_data = json.loads(response)
        return json_data
    except Exception as e:
        logger.error(f"Error extracting structured job data: {e}")
        return {}


def generate_candidate_embedding_text(candidate: FormResponse | Talent) -> str:
    """
    Generate a natural language representation of a candidate's profile for semantic embedding.
    Includes role, years of experience, skills.
    """
    if isinstance(candidate, FormResponse):
        role = candidate.parsed_data.get('Role') or 'an unspecified role'
        skills = candidate.parsed_data.get('Skills', [])
        experience = candidate.parsed_data.get(
            'Years of Experience', 'an unknown number of')
        activities = candidate.parsed_data.get('Activities', [])
        education = candidate.parsed_data.get('Education', 'unspecified')

    elif isinstance(candidate, Talent):
        role = candidate.role or candidate.parsed_role or 'an unspecified role'
        skills = candidate.skills or []
        experience = candidate.years_of_experience or 'an unknown number of'
    else:
        return ""

    skills_text = (
        f"The candidate is skilled in {', '.join(skills)}." if skills else "The candidate's technical skills are unspecified."
    )

    summary = (
        f"This is a candidate applying for {role}. "
        f"They have {experience} years of experience. "
        f"{skills_text}"
    )
    activities_text = (
        f"They have participated in activities such as {', '.join(activities)}." if activities else "No specific activities were mentioned."
    )
    education_text = (
        f"Their educational background includes {education}." if education else "Their educational background is unspecified."
    )

    summary += f" {activities_text} {education_text}"

    return summary.strip()


def create_job_with_automations(title: str, description: str) -> Tuple[Job, List[Dict]]:
    """
    Main MVP function that creates a job and triggers all automations
    """
    # 1. Create and save job
    job = Job.objects.create(title=title, description=description)
    # store structured data in job model
    job.structured_data = get_structured_data_for_job(title, description)
    job.save()

    try:
        # 2. Create Google Form
        form_id, form_url = create_google_form(job)
        permission_body = {
            "type": "domain",
            "role": "writer",   # or "writer"
            "domain": "haya.ng"
        }
        permission_body_2 = {
            'type': 'user',
            'role': 'writer',
            'emailAddress':  "fayemibolu2@gmail.com"
        }
        grant_form_permissions(
            form_id, permission_body)
        grant_form_permissions(
            form_id, permission_body_2)  # Grant permissions to the form

        # 3. Create Google Sheet
        #  sheet_id, sheet_url = create_google_sheet(job, form_id)

        # 4. Post to Twitter
        twitter_post_id = post_job_to_twitter(job, form_url)

        # 5. Update job with generated links
        job.google_form_id = form_id
        job.google_form_url = form_url
        # NOTE:
        # Google Form API does not provide a direct way to link forms to sheets,
        # so we assume the sheet is created and linked automatically.
        # this will be updated in the another process for now

        # job.google_sheet_id = sheet_id
        # job.google_sheet_url = sheet_url

        job.twitter_post_id = twitter_post_id
        job.save()

        # 6. Run candidate matching
        matches = []
        # TODO: revert to real matching logic
        # match_candidates_for_job(job.id)

        logger.info(f"Successfully created job {job.id} with all automations")
        return job, matches

    except Exception as e:
        logger.error(f"Error in job automation for {job.id}: {str(e)}")
        # Job is already created, so we don't delete it, just log the error
        return job, []


def create_google_form(job: Job) -> Tuple[str, str]:
    """
    Create a Google Form for the job posting using real Google Forms API
    """
    logger.info(f"Creating Google Form for job {job.id}")

    try:
        form_id, form_url = create_form(job.title, job.description)
        return form_id, form_url
    except Exception as e:
        logger.error(f"Error creating Google Form for job {job.id}: {str(e)}")
        # Fallback to mock for development if API fails
        form_id = f"mock_form_{job.id}"
        form_url = f"https://forms.google.com/mock/{form_id}"
        return form_id, form_url


def create_google_sheet(job: Job, form_id: str) -> Tuple[str, str]:
    """
    Create a Google Sheet linked to the form using real Google Sheets API
    """
    logger.info(f"Creating Google Sheet for job {job.id}")

    try:
        sheet_id, sheet_url = create_sheet(job.title, form_id)
        return sheet_id, sheet_url
    except Exception as e:
        logger.error(f"Error creating Google Sheet for job {job.id}: {str(e)}")
        # Fallback to mock for development if API fails
        sheet_id = f"mock_sheet_{job.id}"
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        return sheet_id, sheet_url


def post_job_to_twitter(job: Job, form_url: str) -> str:
    """
    Post the job to Twitter with the application form link
    """
    try:
        logger.info(f"Posting job {job.id} to Twitter")

        # Generate tweet content
        tweet_text = generate_job_tweet(job, form_url)

        # Post to Twitter using existing client
        client = Client(
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_KEY_SECRET,
        )

        response = client.create_tweet(text=tweet_text)
        twitter_post_id = response.data['id']

        logger.info(
            f"Successfully posted job {job.id} to Twitter: {twitter_post_id}")
        return twitter_post_id

    except Exception as e:
        logger.error(f"Error posting job {job.id} to Twitter: {str(e)}")
        return ""


def generate_job_tweet(job: Job, form_url: str) -> str:
    """
    Generate optimized tweet content for the job posting
    """
    # Use OpenAI to generate engaging tweet
    prompt = f"""
    Create an engaging Twitter post for this job opening. Include the job title, 
    a brief compelling description, and end with "Apply here: {form_url}".
    Keep it under 240 characters.
    
    Job Title: {job.title}
    Job Description: {job.description[:200]}...
    """

    try:
        response = OpenAPIClient.query(prompt, "", 1)
        tweet_content = response.choices[0].message.content
        return tweet_content
    except Exception as e:
        logger.error(f"Error generating tweet with OpenAI: {str(e)}")
        # Fallback to simple format
        return f"🚀 We're hiring! {job.title}\n\n{job.description[:100]}...\n\nApply here: {form_url}"


def get_job_query_embedding(job: Job) -> List[float]:
    """
    Get the embedding for the job query from cache
    or generate it if not cached.
    """
    job_query = job.get_job_query()
    if not job_query.strip():
        logger.warning(f"Empty job query for job {job.id}")
        return [0.0] * 1536  # Return zero vector if no query

    # Check cache first
    # create hash of the job query to use as key
    job_query_hash = hashlib.sha256(job_query.encode()).hexdigest()
    logger.debug(f"Checking cache for job query embedding: {job_query_hash}")
    cached_embedding = cache.get(job_query_hash)
    if cached_embedding:
        logger.info(f"Using cached embedding for job {job.id}")
        return json.loads(cached_embedding)

    # Generate new embedding
    logger.info(f"Generating new embedding for job {job.id}")
    embedding = get_text_embedding(job_query)
    cache.set(job_query_hash, json.dumps(embedding),
              timeout=settings.JOB_EMBEDDING_CACHE_TTL)  # Cache for 30 days
    return embedding


def match_candidates_for_job(job_id: str) -> List[Dict]:
    """
    Match candidates from talent pool and form responses using AI embeddings
    """
    try:
        job = Job.objects.get(id=job_id)
        logger.info(f"Running candidate matching for job {job.id}")

        # 1. Get job embedding
        job_embedding = get_job_query_embedding(job)

        # 2. Match against talent pool
        talent_matches = match_talent_pool(job, job_embedding)

        # 3. Match against form responses
        form_matches = match_form_responses(job, job_embedding)

        # 4. Combine and save all matches
        all_matches = talent_matches + form_matches
        save_matches_to_db(job, all_matches)

        logger.info(f"Found {len(all_matches)} matches for job {job.id}")
        return all_matches

    except Exception as e:
        logger.error(f"Error matching candidates for job {job_id}: {str(e)}")
        return []


def get_text_embedding(text: str) -> List[float]:
    """
    Get OpenAI embedding for text using real OpenAI API
    """
    try:
        # Use the real OpenAI embeddings API
        embedding = OpenAPIClient.get_embedding(text)
        logger.debug(
            f"Generated embedding of length {len(embedding)} for text: {text[:50]}...")
        return embedding

    except Exception as e:
        logger.error(
            f"Error getting embedding for text '{text[:50]}...': {str(e)}")
        # Return zero vector as fallback
        return [0.0] * 1536


def match_talent_pool(job: Job, job_embedding: List[float]) -> List[Dict]:
    """
    Match candidates from existing talent pool using Pinecone vector search
    """
    matches = []

    try:
        # Use existing Pinecone index for talents
        vector_manager = VectorManager('haya-talents', create_index=False)

        logger.info(
            f"Searching Pinecone for talent matches against job: {job.title}")

        # Search Pinecone for similar talent vectors (top 20 candidates)
        search_results = vector_manager.search(vector=job_embedding, top_k=20)

        logger.info(
            f"Found {len(search_results.matches)} potential matches from Pinecone")

        # Process Pinecone results
        for match in search_results.matches:
            try:
                # Pinecone returns similarity scores (higher = more similar)
                similarity_score = float(match.score)
                talent_id = match.id

                # Apply threshold (Pinecone scores are typically 0-1, higher is better)
                if similarity_score < 0.7:  # Adjust threshold for Pinecone scores
                    logger.info(
                        f"ignore {similarity_score} for talent {talent_id}")
                    continue

                # Fetch talent details from database
                try:
                    talent = Talent.objects.get(id=talent_id)
                except Talent.DoesNotExist:
                    logger.warning(
                        f"Talent {talent_id} found in Pinecone but not in database")
                    continue

                # Extract metadata from Pinecone (includes parsed resume data)
                metadata = match.metadata or {}

                matches.append({
                    'candidate_id': talent.id,
                    'candidate_type': 'talent',
                    'similarity_score': similarity_score,
                    'candidate_data': {
                        'name': f"{talent.first_name} {talent.last_name}",
                        'email': talent.email,
                        'resume_url': talent.resume_url,
                        'skills': metadata.get('skills', talent.skills),
                        'role': metadata.get('role', getattr(talent, 'role', '')),
                        'parsed_role': metadata.get('role', getattr(talent, 'parsed_role', '')),
                        'years_of_experience': metadata.get('years_of_experience', getattr(talent, 'parsed_years_of_experience', '')),
                        'pinecone_metadata': metadata  # Include for debugging
                    }
                })

                logger.debug(
                    f"Talent {talent.id} similarity: {similarity_score:.3f}")

            except Exception as e:
                logger.error(
                    f"Error processing Pinecone match {match.id}: {str(e)}")
                continue

        # Sort by similarity score (already sorted by Pinecone, but ensure order)
        sorted_matches = sorted(
            matches, key=lambda x: x['similarity_score'], reverse=True)
        logger.info(
            f"Found {len(sorted_matches)} talent matches above threshold")

        return sorted_matches

    except Exception as e:
        logger.error(f"Error searching Pinecone for talent matches: {str(e)}")
        return []  # Return empty list if Pinecone fails


def fallback_talent_search(job: Job, job_embedding: List[float]) -> List[Dict]:
    """
    Fallback talent search using database when Pinecone is unavailable
    """
    matches = []
    talents = Talent.objects.all()[:10]  # Limit to avoid performance issues

    logger.info(f"Fallback: Searching {talents.count()} talents from database")

    for talent in talents:
        try:
            # Simple talent text
            talent_text = f"{getattr(talent, 'parsed_role', '')} {getattr(talent, 'skills', '')}"

            if not talent_text.strip():
                continue

            talent_embedding = get_text_embedding(talent_text)
            similarity_score = calculate_similarity(
                job_embedding, talent_embedding)

            if similarity_score > 0.5:
                matches.append({
                    'candidate_id': talent.id,
                    'candidate_type': 'talent',
                    'similarity_score': similarity_score,
                    'candidate_data': {
                        'name': f"{talent.first_name} {talent.last_name}",
                        'email': talent.email,
                        'resume_url': talent.resume_url,
                        'skills': talent.skills,
                    }
                })
        except Exception as e:
            logger.error(
                f"Error in fallback search for talent {talent.id}: {str(e)}")

    return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)


def match_form_responses(job: Job, job_embedding: List[float]) -> List[Dict]:
    """
    Match candidates from form responses using enhanced Pinecone metadata filtering
    """
    matches = []
    form_responses = FormResponse.objects.filter(job=job)

    logger.info(
        f"Matching against {form_responses.count()} form responses for job {job.id}")

    try:
        # Use Pinecone for form responses with enhanced filtering
        vector_manager = VectorManager(
            f'haya-jobs-candidates', create_index=True)

        # Ensure all form responses are in Pinecone with parsed metadata
        for response in form_responses:
            if not response.vector_id:
                add_form_response_to_pinecone(response, vector_manager)

        # Build enhanced Pinecone metadata filters based on job structured data
        pinecone_filter = build_pinecone_form_response_filter(job)

        logger.info(
            f"Using enhanced Pinecone filter for form responses: {pinecone_filter}")

        # Search Pinecone with metadata filtering
        search_results = vector_manager.search(
            vector=job_embedding,
            top_k=10,
            filter=pinecone_filter
        )
        logger.info(
            f"Found {len(search_results.matches)} potential form response matches from Pinecone")

        for match in search_results.matches:
            try:
                similarity_score = float(match.score)
                response_id = match.id

                # Lower threshold for form responses (they applied specifically to this job)
                if similarity_score < 0.6:
                    continue

                # Fetch response details from database
                try:
                    response = FormResponse.objects.get(id=response_id)
                except FormResponse.DoesNotExist:
                    logger.warning(
                        f"Form response {response_id} found in Pinecone but not in database")
                    continue

                metadata = match.metadata or {}
                logger.debug(
                    f"Processing form response {response.id} with metadata: {metadata}")
                matches.append({
                    'candidate_id': response.id,
                    'candidate_type': 'form_response',
                    'similarity_score': similarity_score,
                    'candidate_data': {
                        'name': response.name,
                        'email': response.email,
                        'resume_url': response.resume_url,
                        'phone': response.response_data.get('Phone Number', ''),
                        'years_of_experience': response.response_data.get('Years of Experience', ''),
                        'response_data': response.response_data,
                        'pinecone_metadata': metadata
                    }
                })

                logger.debug(
                    f"Form response {response.id} similarity: {similarity_score:.3f}")

            except Exception as e:
                logger.error(
                    f"Error processing form response match {match.id}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error using Pinecone for form responses: {str(e)}")
        logger.info("Falling back to direct embedding comparison...")
        matches = fallback_form_response_search(
            job, job_embedding, form_responses[:10])

    sorted_matches = sorted(
        matches, key=lambda x: x['similarity_score'], reverse=True)
    logger.info(
        f"Found {len(sorted_matches)} form response matches above threshold")

    return sorted_matches


def build_pinecone_form_response_filter(job: Job) -> Dict[str, Any]:
    """
    Build Pinecone metadata filter for form responses based on job requirements
    Enhanced filtering using job.structured_data
    """
    pinecone_filter = {}
    job_structured_data = job.structured_data or {}

    # Always filter by job_id for form responses
    pinecone_filter['job_id'] = str(job.id)

    # 1. Skills Filtering - Match ANY required skill or technology
    job_skills = job_structured_data.get(
        'skills', []) + job_structured_data.get('technologies', [])
    if job_skills:
        # Normalize skills for consistent filtering
        normalized_skills = [skill.lower().strip()
                             for skill in job_skills if skill]
        if normalized_skills:
            # Use $in operator to match candidates with ANY of the required skills
            pinecone_filter['skills'] = {'$in': normalized_skills}

    # 2. Experience Range Filtering
    job_years_required = job_structured_data.get('years_of_experience')
    if job_years_required and isinstance(job_years_required, (int, float)) and job_years_required > 0:
        # Allow broader range for form responses (±3 years tolerance)
        min_years = max(0, job_years_required - 3)
        max_years = job_years_required + 5  # More lenient on upper bound

        pinecone_filter['years_of_experience'] = {
            '$gte': min_years,
            '$lte': max_years
        }

    # 3. Role Level Filtering (basic level - we'll do advanced filtering in-memory)
    job_role = job_structured_data.get('role', '').lower().strip()
    job_role_level = job_structured_data.get('role_level', '').lower().strip()

    if job_role:
        # Get compatible roles for basic Pinecone filtering
        compatible_roles = get_compatible_roles_for_form_responses(
            job_role, job_role_level)
        if compatible_roles and len(compatible_roles) > 3:
            pinecone_filter['role'] = {'$in': compatible_roles}

    # job_specialization = job_structured_data.get('specialization', '').lower().strip()
    # if job_specialization:
        # Add specialization filtering if specified
        # pinecone_filter['specialization'] = {'$in': [job_specialization]}

    # 4. Education Level Filtering (if we want to be strict about education requirements)
    job_education = job_structured_data.get('education', '').lower().strip()
    if job_education and job_education not in ['not specified', 'any', 'none']:
        # We could add education filtering here, but it might be too restrictive
        pass

    logger.debug(
        f"Built Pinecone filter for form responses: {pinecone_filter}")
    return pinecone_filter


def get_compatible_roles_for_form_responses(job_role: str, job_role_level: str = '') -> List[str]:
    """
    Get compatible roles for form response filtering with role level consideration
    More comprehensive than talent pool filtering since form responses are job-specific
    """
    role_compatibility = {
        'backend': [
            'backend developer', 'backend engineer', 'server developer', 'api developer',
            'python developer', 'django developer', 'nodejs developer', 'java developer',
            'software engineer', 'software developer', 'web developer'
        ],
        'frontend': [
            'frontend developer', 'frontend engineer', 'ui developer', 'ux developer',
            'react developer', 'vue developer', 'angular developer', 'javascript developer',
            'web developer', 'software engineer', 'software developer'
        ],
        'fullstack': [
            'fullstack developer', 'fullstack engineer', 'full stack developer', 'full-stack developer',
            'web developer', 'software engineer', 'software developer',
            'backend developer', 'frontend developer'  # Fullstack can match both
        ],
        'mobile': [
            'mobile developer', 'mobile engineer', 'ios developer', 'android developer',
            'react native developer', 'flutter developer', 'app developer',
            'software engineer', 'software developer'
        ],
        'devops': [
            'devops engineer', 'devops developer', 'infrastructure engineer', 'cloud engineer',
            'site reliability engineer', 'platform engineer', 'deployment engineer',
            'software engineer'
        ],
        'data': [
            'data scientist', 'data engineer', 'data analyst', 'machine learning engineer',
            'ai engineer', 'analytics engineer', 'business intelligence developer',
            # Data roles often overlap with backend
            'software engineer', 'backend developer'
        ],
        'qa': [
            'qa engineer', 'test engineer', 'quality assurance engineer', 'automation engineer',
            'test developer', 'software tester', 'qa analyst'
        ],
        'product': [
            'product manager', 'product owner', 'product specialist', 'product analyst',
            'business analyst', 'project manager'
        ],
        'design': [
            'ui designer', 'ux designer', 'product designer', 'graphic designer',
            'visual designer', 'web designer', 'user experience designer',
            'user interface designer'
        ]
    }

    # Find which category the job role belongs to
    compatible_roles = []
    job_role_lower = job_role.lower()

    for category, roles in role_compatibility.items():
        if any(keyword in job_role_lower for keyword in [category]):
            compatible_roles.extend(roles)
            break

    # If no category matches, try direct role matching with variations
    if not compatible_roles:
        base_role = job_role_lower.replace('senior', '').replace(
            'junior', '').replace('lead', '').strip()
        compatible_roles = [
            base_role
        ]

    # Add role level variations if specified
    if job_role_level and compatible_roles:
        level_variations = []
        for role in compatible_roles:
            level_variations.extend([
                role,  # Keep original
                f"{job_role_level} {role}",
                f"{role} {job_role_level}",
            ])
        compatible_roles.extend(level_variations)

    # Remove duplicates and normalize
    compatible_roles = list(set([role.lower().strip()
                            for role in compatible_roles if role]))

    # Log first 10
    logger.debug(
        f"Compatible roles for '{job_role}' ({job_role_level}): {compatible_roles[:10]}...")
    return compatible_roles


def fallback_form_response_search(job: Job, job_embedding: List[float], form_responses) -> List[Dict]:
    """
    Fallback form response search using direct embedding comparison
    """
    matches = []

    logger.info(
        f"Fallback: Direct embedding comparison for {len(form_responses)} form responses")

    for response in form_responses:
        try:
            # Generate response text for embedding
            response_text = generate_candidate_embedding_text(response)
            if not response_text.strip():
                continue

            response_embedding = get_text_embedding(response_text)
            similarity_score = calculate_similarity(
                job_embedding, response_embedding)

            if similarity_score > 0.5:
                matches.append({
                    'candidate_id': response.id,
                    'candidate_type': 'form_response',
                    'similarity_score': similarity_score,
                    'candidate_data': {
                        'name': response.name,
                        'email': response.email,
                        'resume_url': response.resume_url,
                        'phone': response.response_data.get('Phone Number', ''),
                        'years_of_experience': response.response_data.get('Years of Experience', ''),
                        'response_data': response.response_data,
                    }
                })

        except Exception as e:
            logger.error(
                f"Error in fallback search for form response {response.id}: {str(e)}")

    return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)


def add_form_response_to_pinecone(response: FormResponse, vector_manager: VectorManager) -> str:
    """
    Add a form response to Pinecone vector database with enhanced metadata including parsed resume data
    """
    try:
        # Create comprehensive response text for embedding
        response_text = generate_candidate_embedding_text(response)
        if not response_text.strip():
            return ""

        # Create enhanced metadata for Pinecone filtering, including parsed resume data
        metadata = {
            'name': response.name,
            'email': response.email,
            'years_of_experience_range': response.response_data.get('Years of Experience', ''),
            'job_id': str(response.job.id)
        }

        # Add parsed resume data to metadata if available
        if response.parsed_data:
            # Add role from parsed data
            if response.parsed_data.get('Role'):
                metadata['role'] = response.parsed_data['Role'].lower().strip()

            # Add specialization from parsed data
            if response.parsed_data.get('Specialization'):
                metadata['specialization'] = response.parsed_data['Specialization'].lower(
                ).strip()

            # Add skills from parsed data (normalize to lowercase for filtering)
            if response.parsed_data.get('Skills'):
                metadata['skills'] = [skill.lower().strip()
                                      for skill in response.parsed_data['Skills'] if skill]

            # Add years of experience from parsed data (override form data if available)
            if response.parsed_data.get("Years of Experience") and isinstance(response.parsed_data["Years of Experience"], (int, float)):
                metadata['years_of_experience'] = response.parsed_data["Years of Experience"]

            # Add activities from parsed data
            if response.parsed_data.get('Activities'):
                metadata['activities'] = response.parsed_data['Activities']

            # Add education from parsed data
            if response.parsed_data.get('Education'):
                metadata['education'] = response.parsed_data['Education']

        # Add to Pinecone
        vector_manager.add_text_to_index(
            unique_id=str(response.id),
            text=response_text,
            metadata=metadata
        )

        # Update the response with vector ID
        response.vector_id = str(response.id)
        response.save()

        logger.debug(
            f"Added form response {response.id} to Pinecone with metadata: {metadata}")
        return str(response.id)

    except Exception as e:
        logger.error(
            f"Error adding form response {response.id} to Pinecone: {str(e)}")
        return ""


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings
    """
    return cosine_similarity(embedding1, embedding2)


def save_matches_to_db(job: Job, matches: List[Dict]) -> None:
    """
    Save all matches to the database
    """
    # Clear existing matches for this job
    Match.objects.filter(job=job).delete()

    # Save new matches
    match_objects = []
    for match_data in matches:
        match_obj = Match(
            job=job,
            candidate_id=match_data['candidate_id'],
            candidate_type=match_data['candidate_type'],
            similarity_score=match_data['similarity_score'],
        )
        match_objects.append(match_obj)

    # Bulk create for efficiency
    Match.objects.bulk_create(match_objects)
    logger.info(
        f"Saved {len(match_objects)} matches to database for job {job.id}")


def post_process_form_response(form_response: FormResponse) -> None:
    document_reader = DocumentReader()
    resume_text = document_reader.read_document(
        form_response.resume_url)
    logger.info(
        f"Parsing resume for form response {form_response.id}")
    logger.debug(f"Resume text: {resume_text[:100]}...")
    if not resume_text:
        logger.warning(
            f"No text extracted from resume for form response {form_response.id}")
        return
    parsed_resume_response = parse_candidate_resume(resume_text)
    form_response.parsed_data = {
        'Role': parsed_resume_response.role,
        'Specialization': parsed_resume_response.specialization,
        'Skills': parsed_resume_response.skills,
        'Years of Experience': parsed_resume_response.years_of_experience,
        'Education': parsed_resume_response.education,
        'Activities': parsed_resume_response.activities or []
    }
    form_response.save()


def sync_form_responses(job_id: str) -> int:
    """
    Sync form responses from Google Sheets for a specific job
    """
    try:
        job = Job.objects.get(id=job_id)

        if not job.google_sheet_id:
            logger.warning(f"Job {job.id} has no Google Sheet ID")
            return 0

        # Get responses from Google Sheets
        responses = get_sheet_responses(job.google_sheet_id)

        new_responses = 0
        for response in responses:
            if not response.get('Email Address'):
                continue

            # Check if response already exists
            if not FormResponse.objects.filter(
                job=job,
                email=response.get('Email Address', ''),
                name=response.get('Full Name', '')
            ).exists():
                # Create new FormResponse
                form_response = FormResponse.objects.create(
                    job=job,
                    name=response.get('Full Name', ''),
                    email=response.get('Email Address', ''),
                    resume_url=response.get('Resume/CV', ''),
                    response_data=response
                )
                post_process_form_response(form_response)
                new_responses += 1

        logger.info(f"Synced {new_responses} new responses for job {job.id}")
        return new_responses

    except Exception as e:
        logger.error(
            f"Error syncing form responses for job {job_id}: {str(e)}")
        return 0
