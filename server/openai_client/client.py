from openai import OpenAI
from django.conf import settings


#
class OpenAPIClient:
    client = None

    @staticmethod
    def build_client():
        if OpenAPIClient.client is None:
            OpenAPIClient.client = OpenAI(
                api_key=settings.OPENAPI_API_KEY  # Ensure the setting name is correct
            )
        return OpenAPIClient.client

    @staticmethod
    def query(message: str):
        client = OpenAPIClient.build_client()
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role': 'user',
                'content': message
            }],
            temperature=0.5,
            max_tokens=256,
            n=1,
            stop=None
        )
        # Ensure the response structure is as expected; the path to the message might need adjustments
        return response.choices[0].message
