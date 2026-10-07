"""
main.py
Runs the whole flow:
  Job Description -> structured JD
  resumes/ folder -> read -> parse -> match with JD
  sort by score -> print top 2 and bottom 2
"""
import json
import os
import time

from file_reader import read_resume
from jd_parser import parse_jd
from matcher import final_score
from resume_parser import parse_resume

RESUME_FOLDER = "resumes"
JD_FILE = "sample_jd.txt"
SLEEP_SECONDS = 5   # small pause between LLM calls to avoid API rate limits


def print_candidates(title, candidates):
    print(f"\n===== {title} =====")
    for result in candidates:
        d = result["match"].details
        print(f"\n{d.candidate_name or result['file']}  -  Score: {result['match'].score}/100")
        print(f"  File     : {result['file']}")
        print(f"  Verdict  : {d.verdict}")
        print(f"  Matching : {', '.join(d.matching_skills)}")
        print(f"  Missing  : {', '.join(d.missing_skills)}")


def main():
    # Step 1: read the job description and convert it to structured data
    with open(JD_FILE, "r", encoding="utf-8") as f:
        jd_text = f.read()

    print("Parsing job description...")
    job = parse_jd(jd_text)
    print(f"Role found: {job.role}")
    time.sleep(SLEEP_SECONDS)

    # Step 2: loop through every resume in the folder
    all_results = []
    for file_name in sorted(os.listdir(RESUME_FOLDER)):
        if not file_name.lower().endswith((".pdf", ".docx")):
            continue  # skip anything that is not a PDF/DOCX

        file_path = os.path.join(RESUME_FOLDER, file_name)
        print(f"\nProcessing {file_name} ...")

        try:
            resume_text = read_resume(file_path)

            parsed_resume = parse_resume(resume_text)
            extracted = parsed_resume.model_dump(include={"skills", "projects"})
            print(json.dumps(extracted, indent=2))
            time.sleep(SLEEP_SECONDS)

            match = final_score(job, parsed_resume)
            time.sleep(SLEEP_SECONDS)

            all_results.append({"file": file_name, "match": match})
            print(f"  Score: {match.score}")
        except Exception as error:
            # one bad resume should not stop the whole run
            print(f"  Could not process {file_name}: {error}")

    if not all_results:
        print("No resumes were processed.")
        return

    # Step 3: sort by score (highest first)
    all_results.sort(key=lambda r: r["match"].score, reverse=True)

    # Step 4: print top 2 and bottom 2
    print_candidates("TOP 2 CANDIDATES", all_results[:2])
    print_candidates("BOTTOM 2 CANDIDATES", all_results[-2:])


if __name__ == "__main__":
    main()
