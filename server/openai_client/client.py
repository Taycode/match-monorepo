from openai import OpenAI
from django.conf import settings
import requests


class OpenAPIClient:
    @staticmethod
    def query(message: str):
        api_key = settings.OPENAPI_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": message
            }]
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()  # This will raise an exception for HTTP error responses
            completion_response = response.json()
            return completion_response['choices'][0]['message'] if completion_response['choices'] else None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
#
# class OpenAPIClient:
#     client = None
#
#     @staticmethod
#     def build_client():
#         if OpenAPIClient.client is None:
#             OpenAPIClient.client = OpenAI(
#                 api_key=settings.OPENAPI_API_KEY  # Ensure the setting name is correct
#             )
#         return OpenAPIClient.client
#
#
#     @staticmethod
#     def query(message: str):
#         client = OpenAPIClient.build_client()
#         response = client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=[{
#                 'role': 'user',
#                 'content': message
#             }],
#             temperature=0.5,
#             max_tokens=256,
#             n=1,
#             stop=None
#         )
#         # Ensure the response structure is as expected; the path to the message might need adjustments
#         return response.choices[0].message
#
