from django.db import models


# Create your models here.
class Posting(models.Model):
    source = models.URLField(blank=True)
    post = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
