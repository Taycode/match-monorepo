import json

from openai_client.client import OpenAPIClient
from talents.dataclass import ParsedResumeResponse
from openai_client.schemas.resume_skills_parser import TOOLS as RESUME_SKILLS_PARSER_SCHEMA


# class TalentService:
#     @staticmethod
#     def build_completion_message(query: str):
#         return f"""
#         I want you to return a json (only json) in this format.
#         {{
#         "role": "",
#         "skills": [],
#         "years_of_experience": {{ "gte": "", "lte": "" }},
#         }}
#
#         using this query
#
#         {query}
#         """
#
#     @staticmethod
#     def process_keyword(query: str) -> ParsedResponse:
#         message = TalentService.build_completion_message(query)
#         response = OpenAPIClient.query_for_json(
#             "You are a helpful assistant that can access external functions. You only "
#             "answer in JSON as you are part of an existing strict code base. Not "
#             "applicable fields can be set to null.",
#             message
#         )
#         try:
#             filter_data = json.loads(response.content)
#             role = filter_data.get('role')
#             skills = filter_data.get('skills', [])
#             years_of_experience = filter_data.get('years_of_experience')
#             # remove empty fields
#             years_of_experience = {
#                 key: value
#                 for key, value in years_of_experience.items()
#                 if value
#             }
#         except Exception as e:
#             raise e
#         return ParsedResponse(
#             role=role,
#             skills=skills,
#             years_of_experience=years_of_experience
#         )
#

def build_talent_skill_fetcher_query(resume_text: str) -> str:
    return f"""
            I want you to return a json (only json) in this format.
            {{
            "role": "",
            "skills": [],
            "years_of_experience": int
            }}

            by reading this resume

            {resume_text}
            
            I need the skills to be technical skills (e.g python, figma, etc)
            """


def parse_talent_skills(resume_text: str):
    gpt_query = build_talent_skill_fetcher_query(resume_text)
    response = OpenAPIClient.query_for_json(
        "You are a helpful assistant that can access external functions. You only "
        "answer in JSON as you are part of an existing strict code base. Not "
        "applicable fields can be set to null.",
        gpt_query,
        RESUME_SKILLS_PARSER_SCHEMA
    )
    json_data = json.loads(response)
    role = json_data.get('role')
    skills = json_data.get('skills', [])
    years_of_experience = json_data.get('years_of_experience')
    return ParsedResumeResponse(
        role=role,
        skills=skills,
        years_of_experience=years_of_experience
    )
