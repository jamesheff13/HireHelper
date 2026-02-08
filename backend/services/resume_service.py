# from typing import Optional
# from utils.file_parser import ParsedDocx

# _current_resume: Optional[ParsedDocx] = None

# def set_resume(parsed: ParsedDocx) -> None:
#     global _current_resume
#     _current_resume = parsed

# def get_resume() -> Optional[ParsedDocx]:
#     return _current_resume




# resume_service.py

from typing import Optional
from utils.file_parser import ParsedDocx
import json
import time
from services.ai_service import co, MODEL  # Cohere client

# -----------------------------
# Resume storage
# -----------------------------
_current_resume: Optional[ParsedDocx] = None

def set_resume(parsed: ParsedDocx) -> None:
    """
    Store the parsed resume in memory for later retrieval.
    """
    global _current_resume
    _current_resume = parsed

def get_resume() -> Optional[ParsedDocx]:
    """
    Retrieve the currently stored resume.
    """
    return _current_resume

# -----------------------------
# AI resume analysis
# -----------------------------
def analyze_resume(resume_text: str) -> dict:
    """
    Sends resume_text to Cohere and returns structured feedback:
    overall score + tips per category. Robust to invalid JSON.
    """
    MAX_LENGTH = 3000
    resume_text = resume_text[:MAX_LENGTH]

    prompt = f"""
You are an expert career coach reviewing a resume. Here is the resume content:

{resume_text}

Provide constructive, actionable tips and a score for each section:

Categories:
- Header / Contact Info
- Objective / Summary
- Work Experience
- Skills
- Education / Coursework
- Structure & Formatting

Also give an overall score out of 10.

Respond ONLY in JSON. Use triple backticks around JSON:

{{
"overall_score": "... (num 1-10)",
"tips": {{
"header": {{"tip": "...", "score": "... (num 1-10)"}},
"objective": {{"tip": "...", "score": "... (num 1-10)"}},
"experience": {{"tip": "...", "score": "... (num 1-10)"}},
"skills": {{"tip": "...", "score": "... (num 1-10)"}},
"education": {{"tip": "...", "score": "... (num 1-10)"}},
"structure": {{"tip": "...", "score": "... (num 1-10)"}}
}}
}}

Respond ONLY in JSON.
"""

    for attempt in range(3):
        try:
            response = co.chat(
                model=MODEL,
                message=prompt,
                temperature=0.4,
                max_tokens=450,
            )

            text = response.text.strip()

            # --- robust JSON extraction ---
            start = text.find('{')
            end = text.rfind('}') + 1
            json_text = text[start:end] if start != -1 and end != -1 else ''

            data = json.loads(json_text)
            return data

        except Exception as e:
            print(f"[Resume AI error attempt {attempt+1}]:", e)
            time.sleep(0.5)

    # fallback if AI fails
    return {
        "overall_score": "N/A",
        "tips": {
            "header": {"tip": "No feedback available", "score": "N/A"},
            "objective": {"tip": "No feedback available", "score": "N/A"},
            "experience": {"tip": "No feedback available", "score": "N/A"},
            "skills": {"tip": "No feedback available", "score": "N/A"},
            "education": {"tip": "No feedback available", "score": "N/A"},
            "structure": {"tip": "No feedback available", "score": "N/A"},
        },
    }
