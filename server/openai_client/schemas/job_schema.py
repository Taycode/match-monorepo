JOB_PARSER_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "structured_job_data",
        "description": "This schema is used to extract structured data from job.",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The job title extracted from the job description."
                },
                "role": {
                    "type": "string",
                    "description": "The job role extracted from the job. "
                },
                "role_level": {
                    "type": "string",
                    "description": "The level of the job role, such as 'junior', 'mid', or 'senior'.",
                    "enum": [
                        "intern",
                        "junior",
                        "mid",
                        "senior",
                        "lead",
                    ]
                },
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of technical skills extracted from the job."
                },
                "technologies": {
                    "type": "array",
                    "description": "List of specific technologies mentioned",
                    "items": {
                        "type": "string",
                        "minLength": 1,
                        "description": "A technology name, tool, or framework"
                    },
                },
                "years_of_experience": {
                    "type": "integer",
                    "description": "The number of years of experience extracted from the resume."
                },
                "education": {
                    "type": "string",
                    "description": "The lowest level of education required as extracted from the job."
                },
                "responsibilities_summary": {
                    "type": "string",
                    "description": "A summary of the job responsibilities. "
                    "This should be a concise overview of the main tasks and duties associated with the job."
                },
                "location": {
                    "type": "string",
                    "description": "Workplace setting: remote, on-site, or hybrid",
                    "enum": [
                        "remote",
                        "on-site",
                        "hybrid"
                    ]
                },
            },
            "required": ["title", "role",  "role_level",
                         "skills", "technologies", "years_of_experience",
                         "education", "location", "responsibilities_summary"],
            "additionalProperties": False
        }
    },
}
