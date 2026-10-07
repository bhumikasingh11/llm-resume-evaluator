"""
jd_parser.py
Turns an unstructured Job Description (plain text) into a JobDescription object.
"""

import json

from llm import ask_llm_for_json
from models import JobDescription


def parse_jd(jd_text):
    # The schema is shown to the LLM so it knows exactly what JSON to return
    schema = json.dumps(JobDescription.model_json_schema(), indent=2)

    system_prompt = f"""You are an expert recruiter who extracts information from job descriptions.

Rules:
- Return ONLY valid JSON. No explanation, no markdown.
- Follow this JSON schema exactly:
{schema}
- Extract the actual information from the job description.
- Do NOT invent information that is not in the job description.
- If minimum experience is not mentioned, return null for minimum_experience.
"""

    user_prompt = f"Job Description:\n{jd_text}"

    return ask_llm_for_json(system_prompt, user_prompt, JobDescription)
