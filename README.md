# LLM Resume Evaluator

A small learning project from my AI Engineering course (Week 1, Day 7).
It is **not** a production HR tool - just practice with LLMs and structured output.

## What the project does
- Reads a Job Description and converts it into structured JSON using an LLM.
- Reads resumes (PDF / DOCX) from the `resumes/` folder and converts each into structured JSON.
- Uses an LLM as a recruiter to score each resume (0-100) against the job.
- Ranks candidates and prints the top 2 and bottom 2.

## Technologies / concepts learned
- Python, OpenAI-compatible LLM API
- Prompt engineering (asking for JSON only, "do not invent information")
- Pydantic models for structured output and validation
- Reading PDF (`pypdf`) and DOCX (`python-docx`, including tables)
- `time.sleep()` to avoid API rate limits

## Project flow
```
sample_jd.txt -> parse_jd() -> JobDescription
resumes/*.pdf|docx -> read_resume() -> parse_resume() -> Resume
JobDescription + Resume -> final_score() -> MatchResult
sort by score -> TOP 2 / BOTTOM 2
```

## Setup
```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # then put your API key in .env
```

## How to run
```
python main.py
```
Put your own resumes (PDF/DOCX) in the `resumes/` folder and edit `sample_jd.txt` for a different job.

## Example output
```
===== TOP 2 CANDIDATES =====

Aarav Sharma  -  Score: 88/100
  File     : resume1.pdf
  Verdict  : Strong backend profile that meets almost every requirement.
  Matching : Python, REST APIs, SQL, Git
  Missing  : AWS

===== BOTTOM 2 CANDIDATES =====
...
```
(Your scores and wording will differ - the LLM generates them.)
