"""
llm.py
One small helper that talks to the LLM.
It uses the OpenAI-compatible client, so you can switch provider/model
just by changing values in your .env file (no code change needed).
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Read the .env file so os.getenv() can see the values
load_dotenv()

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")          # optional (needed for non-OpenAI providers)
model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")

if not api_key:
    raise ValueError("LLM_API_KEY is missing. Copy .env.example to .env and add your key.")

client = OpenAI(api_key=api_key, base_url=base_url)


def ask_llm_for_json(system_prompt, user_prompt, model_class):
    """
    Sends a prompt to the LLM, expects JSON back,
    and converts it into the given Pydantic model class.
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,  # 0 = most predictable answers
    )

    text = response.choices[0].message.content.strip()

    # Some models wrap JSON in ```json ... ``` - remove that if present
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()

    data = json.loads(text)                 # text -> Python dict
    return model_class(**data)              # dict -> validated Pydantic object
