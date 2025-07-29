from django.db import models
from ulid2 import generate_ulid_as_uuid


# Create your models here.
class Posting(models.Model):
    id = models.UUIDField(
        max_length=100,  # ULIDs (in Base32) are 26 characters long
        primary_key=True,
        default=generate_ulid_as_uuid
    )
    source = models.URLField(max_length=1000, blank=True)
    post = models.TextField(max_length=5000)
    generated_tweet = models.TextField(max_length=1000)
    edited_tweet = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# MVP Job Posting Model
class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=generate_ulid_as_uuid,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Store structured data from job description
    structured_data = models.JSONField(default=dict)

    # Google integrations
    google_form_id = models.CharField(max_length=255, blank=True, null=True)
    google_form_url = models.URLField(blank=True, null=True)
    google_sheet_id = models.CharField(max_length=255, blank=True, null=True)
    google_sheet_url = models.URLField(blank=True, null=True)

    # Twitter integration
    twitter_post_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_job_query(self):
        """
        Returns a query string for the job title and description.
        This can be used for searching or indexing purposes.
        """
        if not self.structured_data:
            return f"{self.title} {self.description}"
        job_query = f"{self.structured_data.get('title', '')} {self.structured_data.get('description', '')}"
        job_query += f"We’re hiring a {self.title}."

        job_query += "Requirements: "
        job_query += f"- {self.structured_data.get('years_of_experience', '')} years of experience "
        job_query += f"in {self.structured_data.get('role', '')}."
        job_query += f"- Strong knowledge of {''.join(self.structured_data.get('skills', []))}."
        job_query += f"- {self.structured_data.get('education', '')} education is required. "
        job_query += f"- Experience with {''.join(self.structured_data.get('technologies', []))}."
        return job_query.strip()

    def get_job_query(self):
        data = self.structured_data or {}

        title = data.get('title', self.title or '')
        description = data.get('description', self.description or '')
        role = data.get('role', '')
        experience = data.get('years_of_experience', '')
        skills = ', '.join(data.get('skills', []))
        technologies = ', '.join(data.get('technologies', []))
        education = data.get('education', '')
        responsibilities_summary = data.get('responsibilities_summary', '')

        query = f"""
        We are hiring a {title}. {description.strip()}

        This role requires at least {experience} years of experience in {role}.  
        Ideal candidates should be proficient in {skills}, and have hands-on experience with {technologies}.

        {responsibilities_summary}

        A background in {education} is preferred.
        """.strip()
        return query


# Form responses from Google Forms
class FormResponse(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=generate_ulid_as_uuid,
        editable=False
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='form_responses')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_url = models.URLField(blank=True, null=True)
    response_data = models.JSONField(default=dict)  # Store all form data
    # Store parsed data for easier access
    parsed_data = models.JSONField(default=dict)
    vector_id = models.CharField(
        max_length=255, blank=True, null=True)  # Pinecone vector ID
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'form_responses'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.job.title}"


# Candidate matches for jobs
class Match(models.Model):
    CANDIDATE_TYPES = [
        ('talent', 'Talent Pool'),
        ('form_response', 'Form Response'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=generate_ulid_as_uuid,
        editable=False
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='matches')
    candidate_id = models.UUIDField()  # References either Talent or FormResponse
    candidate_type = models.CharField(max_length=20, choices=CANDIDATE_TYPES)
    similarity_score = models.FloatField(null=True, blank=True)
    is_shortlisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'matches'
        ordering = ['-similarity_score']
        unique_together = ['job', 'candidate_id', 'candidate_type']

    def __str__(self):
        return f"Match for {self.job.title} - {self.candidate_type}"
