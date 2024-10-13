import json

from openai_client.client import OpenAPIClient
from talents.dataclass import ParsedResponse


class TalentService:
    @staticmethod
    def build_completion_message(query: str):
        return f"""
        I want you to return a json (only json) in this format.
        {{
        "role": "",
        "skills": [],
        "years_of_experience": {{ "gte": "", "lte": "" }},
        }}
                
        using this query
        
        {query}
        """

    @staticmethod
    def process_keyword(query: str) -> ParsedResponse:
        message = TalentService.build_completion_message(query)
        response = OpenAPIClient.query_for_json(
            "You are a helpful assistant that can access external functions. You only "
            "answer in JSON as you are part of an existing strict code base. Not "
            "apllicable fields can be set to null.",
            message
        )
        try:
            filter_data = json.loads(response.content)
            role = filter_data.get('role')
            skills = filter_data.get('skills', [])
            years_of_experience = filter_data.get('years_of_experience')
            # remove empty fields
            years_of_experience = {
                key: value
                for key, value in years_of_experience.items()
                if value
            }
        except Exception as e:
            raise e
        return ParsedResponse(
            role=role,
            skills=skills,
            years_of_experience=years_of_experience
        )
