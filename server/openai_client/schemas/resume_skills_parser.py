TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "return_structured_job_search_query",
            "description": "Return the structured json of the search query. Separate query into role, skills and years_of_experience. The json returned will be used to search a backend service using elasticsearch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Examples: Backend Engineer, Software Engineer, Developer (without the skill or language). The role from the search query. . Never like this 'Python Backend Engineer',",
                    },
                    "skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The skills and languages mentioned in the search query. e.g. Python, Django.",
                    },
                    "years_of_experience": {
                        "type": "object",
                        "items": {
                            "type": "integer"
                        },
                        "description": "The years of experience given in the query.",
                    }
                }, "required": ["role", "skills", "years_of_experience"]
            }
        }
    }
]
