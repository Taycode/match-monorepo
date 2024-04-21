from openai import OpenAI
from django.conf import settings
from .schemas import TOOLS

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
            temperature=0.1,
            response_format={
                "type": "json_object", 
            },
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can access external functions. You only answer in JSON as you are part of an existing strict code base. Not apllicable fields can be set to null."},
                {'role': 'user', 'content': message}
            ],
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=256,
            n=1,
            stop=None
        )
        # Ensure the response structure is as expected; the path to the message might need adjustments
        return response.choices[0].message.model_dump()['tool_calls'][0]['function']['arguments']