from openai import OpenAI
from django.conf import settings
import logging
import tiktoken  # Install with: pip install tiktoken

logger = logging.getLogger(__name__)


class OpenAPIClient:
    client = None

    @staticmethod
    def build_client():
        """
        Builds and caches the OpenAI client using the provided API key.
        """
        if OpenAPIClient.client is None:
            api_key = getattr(settings, 'OPENAPI_API_KEY', None)
            if not api_key:
                logger.error("OPENAPI_API_KEY is not set in settings.")
                raise ValueError("OPENAPI_API_KEY is missing from settings.")
            OpenAPIClient.client = OpenAI(api_key=api_key)
        return OpenAPIClient.client

    @staticmethod
    def estimate_tokens(messages, model="gpt-4o-mini"):
        """
        Estimate the number of tokens in the provided messages using tiktoken.
        """
        encoder = tiktoken.encoding_for_model(model)
        token_count = 0
        for msg in messages:
            token_count += len(encoder.encode(msg["content"]))
        return token_count

    @staticmethod
    def truncate_message(content, model="gpt-4o-mini", max_tokens=1000):
        """
        Truncate a message to fit within the maximum token count.
        """
        encoder = tiktoken.encoding_for_model(model)
        tokens = encoder.encode(content)
        if len(tokens) > max_tokens:
            truncated_content = encoder.decode(tokens[:max_tokens])
            return truncated_content
        return content

    @staticmethod
    def query_for_json(prompt: str, message: str, schema: list):
        """
        Queries the OpenAI API and returns a JSON response based on the schema.
        """
        client = OpenAPIClient.build_client()
        max_context_tokens = 128000  # Model-specific max tokens
        max_response_tokens = 256  # Reserve tokens for the response
        max_input_tokens = max_context_tokens - max_response_tokens

        # Prepare messages
        system_message = {"role": "system", "content": prompt}
        user_message = {"role": "user", "content": message}
        messages = [system_message, user_message]

        # Estimate and truncate if necessary
        token_count = OpenAPIClient.estimate_tokens(messages)
        if token_count > max_input_tokens:
            logger.warning(f"Input token count ({token_count}) exceeds limit ({max_input_tokens}). Truncating messages.")
            user_message["content"] = OpenAPIClient.truncate_message(
                user_message["content"], max_tokens=max_input_tokens // 2
            )
            system_message["content"] = OpenAPIClient.truncate_message(
                system_message["content"], max_tokens=max_input_tokens // 2
            )
            messages = [system_message, user_message]

        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                temperature=0.1,
                response_format={
                    "type": "json_object",
                },
                messages=messages,
                tools=schema,
                tool_choice="auto",
                max_tokens=max_response_tokens,
                n=1,
                stop=None
            )
            # Access response attributes directly
            choice = response.choices[0]
            message_content = choice.message
            tool_calls = message_content.tool_calls

            # Validate and extract tool call arguments
            if tool_calls and hasattr(tool_calls[0], "function"):
                return tool_calls[0].function.arguments
            else:
                raise ValueError("Unexpected response structure from OpenAI API.")
        except Exception as e:
            logger.error(f"Error querying OpenAI API: {e}")
            raise ValueError(f"Failed to query OpenAI API: {e}")

    @staticmethod
    def query(prompt: str, message: str, number_of_responses: int = 1):
        """
        Queries the OpenAI API for general completions and returns the response.
        """
        client = OpenAPIClient.build_client()
        max_context_tokens = 128000  # Model-specific max tokens
        max_response_tokens = 256  # Reserve tokens for the response
        max_input_tokens = max_context_tokens - max_response_tokens

        # Prepare messages
        system_message = {"role": "system", "content": prompt}
        user_message = {"role": "user", "content": message}
        messages = [system_message, user_message]

        # Estimate and truncate if necessary
        token_count = OpenAPIClient.estimate_tokens(messages)
        if token_count > max_input_tokens:
            logger.warning(f"Input token count ({token_count}) exceeds limit ({max_input_tokens}). Truncating messages.")
            user_message["content"] = OpenAPIClient.truncate_message(
                user_message["content"], max_tokens=max_input_tokens // 2
            )
            system_message["content"] = OpenAPIClient.truncate_message(
                system_message["content"], max_tokens=max_input_tokens // 2
            )
            messages = [system_message, user_message]

        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=messages,
                n=number_of_responses,
                stop=None
            )
            return response
        except Exception as e:
            logger.error(f"Error querying OpenAI API: {e}")
            raise ValueError(f"Failed to query OpenAI API: {e}")
