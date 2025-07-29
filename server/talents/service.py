import json

from common.utils.document_reader import DocumentReader
from openai_client.client import OpenAPIClient
from talents.dataclass import ParsedResumeResponse
from openai_client.schemas.resume_schema import RESUME_PARSER_SCHEMA
from talents.models import Talent
from vector.service import VectorManager
from dataclasses import asdict

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


def parse_candidate_resume(resume_text: str):
    try:
        response = OpenAPIClient.query_for_json(
            "You are an expert at structured data extraction. "
            "You will be given unstructured candidate's resume text"
            "and should convert it into the given structure."
            "Not applicable fields can be set to null."
            "Ensure the skills are technical skills (e.g python, figma, etc)"
            "Ensure the extracted data is relevant to "
            "or inferred from the candidate's resume."
            "Extract a clear short summary of what this candidate has done"
            "in previous roles: key responsibilities, duties, "
            "and tasks as activities."
            "max 2-3 short sentences.",
            resume_text,
            RESUME_PARSER_SCHEMA
        )
        print(f"Parsed resume response: {response}")
        json_data = json.loads(response)
        print(f"Parsed resume data: {json_data}")
        role = json_data.get('role')
        skills = json_data.get('skills', [])
        years_of_experience = json_data.get('years_of_experience')
        activities = json_data.get('activities', [])
        education = json_data.get('education', None)
        return ParsedResumeResponse(
            role=role,
            skills=skills,
            years_of_experience=years_of_experience,
            activities=activities,
            education=education
        )
    except Exception as e:
        print(f"Error parsing candidate resume: {e}")
        return ParsedResumeResponse(
            role=None,
            skills=[],
            years_of_experience=0,
            activities=[],
            education=None
        )


def post_process_new_talent(talent: Talent):
    """"
    This processes new talents added to the pool to enable proper search when job matching

    It follows the following steps
    1. Parse role and skills and store in DB
    2. Upsert data into pinecone
    """
    document_reader = DocumentReader()
    resume_text = document_reader.read_document(talent.resume_url)
    parsed_resume_response = parse_candidate_resume(resume_text)
    talent.parsed_role = parsed_resume_response.role
    talent.skills = parsed_resume_response.skills
    talent.parsed_years_of_experience = parsed_resume_response.years_of_experience
    talent.save()

    vector_manager = VectorManager('haya-talents')
    vector_manager.add_text_to_index(
        unique_id=str(talent.id),
        text=resume_text,
        metadata=asdict(parsed_resume_response)
    )
