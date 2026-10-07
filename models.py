"""
models.py
All Pydantic models live here.
Pydantic lets us define the SHAPE of our data and validates it for us.
"""

from typing import List, Optional
from pydantic import BaseModel


# ---------- Job Description ----------

class JobDescription(BaseModel):
    role: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    minimum_experience: Optional[float] = None   # in years, null if not mentioned
    educational_requirements: Optional[str] = None
    responsibilities: List[str] = []


# ---------- Resume ----------

class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    skills_used: List[str] = []


class Resume(BaseModel):
    # Everything is optional because every resume looks different
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    total_experience_years: Optional[float] = None
    skills: List[str] = []
    experiences: List[Experience] = []
    projects: List[str] = []
    certifications: List[str] = []
    achievements: List[str] = []


# ---------- Match Result ----------

class MatchDetails(BaseModel):
    candidate_name: Optional[str] = None
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    experience_match: Optional[str] = None   # e.g. "Meets requirement (3 yrs vs 2 yrs)"
    strengths: List[str] = []
    weaknesses: List[str] = []
    verdict: Optional[str] = None            # short comment


class MatchResult(BaseModel):
    score: int            # 0 - 100
    details: MatchDetails
