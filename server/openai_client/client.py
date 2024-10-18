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
    def query_for_json(prompt: str, message: str):
        client = OpenAPIClient.build_client()
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            temperature=0.1,
            response_format={
                "type": "json_object", 
            },
            messages=[
                {"role": "system", "content": prompt},
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

    @staticmethod
    def query(prompt: str, message: str):
        client = OpenAPIClient.build_client()
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": prompt},
                {'role': 'user', 'content': message}
            ],
            max_tokens=70,
            n=1,
            stop=None
        )
        # Ensure the response structure is as expected; the path to the message might need adjustments
        return response.choices[0].message
