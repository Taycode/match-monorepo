import json
import logging
from typing import List, Dict, Any, Tuple
from django.conf import settings

from tweepy import Client
from openai_client.client import OpenAPIClient
from postings.models import Job, FormResponse, Match
from talents.models import Talent

logger = logging.getLogger(__name__)


def create_job_with_automations(title: str, description: str) -> Tuple[Job, List[Dict]]:
    """
    Main MVP function that creates a job and triggers all automations
    """
    # 1. Create and save job
    job = Job.objects.create(title=title, description=description)
    
    try:
        # 2. Create Google Form
        form_id, form_url = create_google_form(job)
        
        # 3. Create Google Sheet
        sheet_id, sheet_url = create_google_sheet(job, form_id)
        
        # 4. Post to Twitter
        twitter_post_id = post_job_to_twitter(job, form_url)
        
        # 5. Update job with generated links
        job.google_form_id = form_id
        job.google_form_url = form_url
        job.google_sheet_id = sheet_id
        job.google_sheet_url = sheet_url
        job.twitter_post_id = twitter_post_id
        job.save()
        
        # 6. Run candidate matching
        matches = match_candidates_for_job(job.id)
        
        logger.info(f"Successfully created job {job.id} with all automations")
        return job, matches
        
    except Exception as e:
        logger.error(f"Error in job automation for {job.id}: {str(e)}")
        # Job is already created, so we don't delete it, just log the error
        return job, []


def create_google_form(job: Job) -> Tuple[str, str]:
    """
    Create a Google Form for the job posting
    TODO: Replace with actual Google Forms API integration
    """
    # For MVP, we'll mock this - replace with real Google Forms API
    logger.info(f"Creating Google Form for job {job.id}")
    
    # Mock implementation - replace with real Google Forms API
    form_id = f"mock_form_{job.id}"
    form_url = f"https://forms.google.com/mock/{form_id}"
    
    # Real implementation would look like:
    # from google.oauth2.credentials import Credentials
    # from googleapiclient.discovery import build
    # 
    # service = build('forms', 'v1', credentials=creds)
    # form_body = {
    #     "info": {
    #         "title": f"Application for {job.title}",
    #         "description": f"Please fill out this form to apply for: {job.title}"
    #     }
    # }
    # form = service.forms().create(body=form_body).execute()
    # return form['formId'], form['responderUri']
    
    return form_id, form_url


def create_google_sheet(job: Job, form_id: str) -> Tuple[str, str]:
    """
    Create a Google Sheet linked to the form
    TODO: Replace with actual Google Sheets API integration
    """
    logger.info(f"Creating Google Sheet for job {job.id}")
    
    # Mock implementation - replace with real Google Sheets API
    sheet_id = f"mock_sheet_{job.id}"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    
    # Real implementation would look like:
    # from googleapiclient.discovery import build
    # 
    # service = build('sheets', 'v4', credentials=creds)
    # spreadsheet_body = {
    #     'properties': {
    #         'title': f"Applications for {job.title}"
    #     }
    # }
    # spreadsheet = service.spreadsheets().create(body=spreadsheet_body).execute()
    # return spreadsheet['spreadsheetId'], spreadsheet['spreadsheetUrl']
    
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
            bearer_token=settings.TWITTER_BEARER_TOKEN,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_KEY_SECRET,
        )
        
        response = client.create_tweet(text=tweet_text)
        twitter_post_id = response.data['id']
        
        logger.info(f"Successfully posted job {job.id} to Twitter: {twitter_post_id}")
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


def match_candidates_for_job(job_id: str) -> List[Dict]:
    """
    Match candidates from talent pool and form responses using AI embeddings
    """
    try:
        job = Job.objects.get(id=job_id)
        logger.info(f"Running candidate matching for job {job.id}")
        
        # 1. Get job embedding
        job_text = f"{job.title} {job.description}"
        job_embedding = get_text_embedding(job_text)
        
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
    Get OpenAI embedding for text
    TODO: Replace with actual OpenAI embeddings API
    """
    try:
        # Mock implementation - replace with real OpenAI embeddings
        # response = openai.Embedding.create(
        #     model="text-embedding-3-small",
        #     input=text
        # )
        # return response['data'][0]['embedding']
        
        # Return mock embedding for now
        return [0.1] * 1536  # text-embedding-3-small returns 1536 dimensions
        
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        return [0.0] * 1536


def match_talent_pool(job: Job, job_embedding: List[float]) -> List[Dict]:
    """
    Match candidates from existing talent pool
    """
    matches = []
    talents = Talent.objects.all()
    
    for talent in talents:
        # Get talent embedding
        talent_text = f"{talent.role} {' '.join(talent.skills or [])}"
        talent_embedding = get_text_embedding(talent_text)
        
        # Calculate similarity (mock for now)
        similarity_score = calculate_similarity(job_embedding, talent_embedding)
        
        if similarity_score > 0.5:  # Threshold for matching
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
    
    return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)


def match_form_responses(job: Job, job_embedding: List[float]) -> List[Dict]:
    """
    Match candidates from form responses
    """
    matches = []
    form_responses = FormResponse.objects.filter(job=job)
    
    for response in form_responses:
        # Get response embedding
        response_text = f"{response.name} {response.response_data.get('skills', '')}"
        response_embedding = get_text_embedding(response_text)
        
        # Calculate similarity
        similarity_score = calculate_similarity(job_embedding, response_embedding)
        
        if similarity_score > 0.5:  # Threshold for matching
            matches.append({
                'candidate_id': response.id,
                'candidate_type': 'form_response',
                'similarity_score': similarity_score,
                'candidate_data': {
                    'name': response.name,
                    'email': response.email,
                    'resume_url': response.resume_url,
                    'skills': response.response_data.get('skills', []),
                }
            })
    
    return sorted(matches, key=lambda x: x['similarity_score'], reverse=True)


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings
    TODO: Replace with actual similarity calculation
    """
    # Mock similarity calculation - replace with real cosine similarity
    import random
    return random.uniform(0.3, 0.9)  # Mock similarity score


def save_matches_to_db(job: Job, matches: List[Dict]) -> None:
    """
    Save all matches to the database
    """
    for match_data in matches:
        Match.objects.get_or_create(
            job=job,
            candidate_id=match_data['candidate_id'],
            candidate_type=match_data['candidate_type'],
            defaults={
                'similarity_score': match_data['similarity_score']
            }
        )


def sync_form_responses(job_id: str) -> int:
    """
    Sync new responses from Google Sheets
    TODO: Replace with actual Google Sheets API integration
    """
    try:
        job = Job.objects.get(id=job_id)
        logger.info(f"Syncing form responses for job {job.id}")
        
        # Mock implementation - replace with real Google Sheets API
        # service = build('sheets', 'v4', credentials=creds)
        # result = service.spreadsheets().values().get(
        #     spreadsheetId=job.google_sheet_id,
        #     range='A:Z'
        # ).execute()
        # values = result.get('values', [])
        
        # For now, return 0 new responses
        return 0
        
    except Exception as e:
        logger.error(f"Error syncing form responses for job {job_id}: {str(e)}")
        return 0 