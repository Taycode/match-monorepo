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

