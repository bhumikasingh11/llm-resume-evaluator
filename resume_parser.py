"""
resume_parser.py
Turns raw resume text into a structured Resume object.
"""

import json

from llm import ask_llm_for_json
from models import Resume


def parse_resume(resume_text):
    schema = json.dumps(Resume.model_json_schema(), indent=2)

    system_prompt = f"""You are an expert resume parser.

Rules:
- Return ONLY valid JSON. No explanation, no markdown.
- Follow this JSON schema exactly:
{schema}
- Resumes use different headings. Treat headings like "Experience",
  "Professional Experience", "Work History", "Employment" and "Internship"
  as work experience and put them in "experiences".
- Do NOT invent information. If something is missing, use null (or an empty list).
- total_experience_years should be a number (e.g. 2.5). Estimate it from the
  work experience dates only if they are clearly given, otherwise null.
"""

    user_prompt = f"Resume text:\n{resume_text}"

    return ask_llm_for_json(system_prompt, user_prompt, Resume)
