from dataclasses import dataclass


@dataclass
class ParsedResponse:
    role: str
    skills: list
    years_of_experience: dict
