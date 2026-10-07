"""
matcher.py
Compares a structured Job Description with a structured Resume
and returns a MatchResult (score + details).
"""

import json

from llm import ask_llm_for_json
from models import MatchResult


def final_score(job, parsed_resume):
    schema = json.dumps(MatchResult.model_json_schema(), indent=2)

    system_prompt = f"""You are an experienced HR recruiter.
Compare the candidate's resume with the job description.

Rules:
- Return ONLY valid JSON. No explanation, no markdown.
- Follow this JSON schema exactly:
{schema}
- score must be an integer from 0 to 100.
- Judge only from the information given. Do not invent facts.
- Fill matching_skills, missing_skills, experience_match, strengths,
  weaknesses and a short verdict in details.
"""

    # model_dump_json() converts a Pydantic object into a JSON string
    user_prompt = f"""JOB DESCRIPTION:
{job.model_dump_json(indent=2)}

CANDIDATE RESUME:
{parsed_resume.model_dump_json(indent=2)}
"""

    return ask_llm_for_json(system_prompt, user_prompt, MatchResult)
