from django.db.models.signals import post_save
from django.dispatch import receiver
from postings.models import Posting
from postings.services import trigger_post_on_twitter


@receiver(post_save, sender=Posting)
def tweet_posting(sender, instance, **kwargs):
    trigger_post_on_twitter(instance)
