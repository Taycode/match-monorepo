RESUME_PARSER_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "structured_resume_data",
        "description": "This schema is used to extract structured data from resumes, including role",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "The job role extracted from the resume.e.g Backend Developer, Frontend Developer, Fullstack Developer, etc."
                },
                "specialization": {
                    "type": "string",
                    "description": "The specialization of the resume, such as"
                    "'backend', 'frontend', 'fullstack', 'mobile', 'web', 'api', 'database',"
                    "'distributed system', 'microservices', 'cloud', 'infrastructure'"
                },
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of technical skills extracted from the resume."
                },
                "years_of_experience": {
                    "type": "integer",
                    "description": "The number of years of experience extracted from the resume."
                },
                "education": {
                    "type": "string",
                    "description": "The education or degree as extracted from the resume."
                },
                "activities": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Key summary of activities or responsibilities in previous work experience."
                    },
                    "description": "A list of responsibilities or activities done in previous work experience."
                }
            },
            "required": ["role", "specialization", "skills", "years_of_experience", "activities", "education"],
            "additionalProperties": False}
    }
}
