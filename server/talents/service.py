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
        "years_of_experience": "",
        }}
        where years of experience is >=5 for minimum of 5 years and <=5 for less than 5 years.
        
        using this query
        
        {query}
        """

    @staticmethod
    def process_keyword(query: str) -> ParsedResponse:
        message = TalentService.build_completion_message(query)
        response = OpenAPIClient.query(message)
        print(response)
        try:
            filter_data = {}
            role = filter_data.get('role')
            skills = filter_data.get('skills', [])
            years_of_experience = filter_data.get('years_of_experience')
        except Exception as e:
            raise e
        return ParsedResponse(
            role=role,
            skills=skills,
            years_of_experience=years_of_experience
        )
