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


# Form responses from Google Forms
class FormResponse(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=generate_ulid_as_uuid,
        editable=False
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='form_responses')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume_url = models.URLField(blank=True, null=True)
    response_data = models.JSONField(default=dict)  # Store all form data
    vector_id = models.CharField(max_length=255, blank=True, null=True)  # Pinecone vector ID
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
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='matches')
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

