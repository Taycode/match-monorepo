import json

from tweepy import Client
from django.conf import settings

from openai_client.client import OpenAPIClient
from postings.models import Posting


def post_tweet(text: str):
    client = Client(
        bearer_token=settings.TWITTER_BEARER_TOKEN,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_KEY_SECRET,
    )
    client.create_tweet(text=text)


def generate_tweet_for_posting(posting: Posting):
    prompt = """I have a stringified JSON object that contains a job posting with a 'text' field and an optional 
    'source' field (which may be a URL or empty). Summarize the 'text' field into a concise version that is no longer 
    than 250 characters, focusing on key details like the job title, company name, location (if applicable), 
    and qualifications. If the 'source' field contains a URL, append it at the end of the summary. If the 'source' 
    field is empty, leave it out."""
    input_data = json.dumps({
        'text': posting.post,
        'source': posting.source,
    })
    response = OpenAPIClient.query(
        prompt,
        input_data,
    )
    return response.content


def trigger_post_on_twitter(posting: Posting):
    tweet = generate_tweet_for_posting(posting)
    post_tweet(tweet)
