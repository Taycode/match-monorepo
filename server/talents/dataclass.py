from dataclasses import dataclass


@dataclass
class ParsedResumeResponse:
    role: str
    skills: list
    years_of_experience: int
    activities: list
    education: str = None
    
