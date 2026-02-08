#all AI calls

import os
import cohere
import time
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

MODEL = "command-xlarge-nightly"  # valid model as of 2026

def generate_question(role, history):
    asked = {q.lower() for q, _ in history}
    prompt = f"""
You are a professional interviewer for a {role}.
Previously asked questions: {', '.join(q for q, _ in history) or 'None'}
Ask ONE new interview question. Questions can be behavioral and/or technical. 
Do NOT repeat previous questions. Respond ONLY with the question text.
"""
    try:
        response = co.chat(model=MODEL, message=prompt, temperature=0.8, max_tokens=80)
        question = response.text.strip()
        if question.lower() not in asked:
            return question
    except Exception as e:
        print("[AI ERROR]", e)

    # Fallback questions
    FALLBACKS = [
        "What interests you most about this role?",
        "Tell me about a challenge you handled successfully.",
        "How do you approach learning something new?",
        "Describe a time you received constructive criticism.",
        "What strengths do you bring to a team?"
    ]
    for q in FALLBACKS:
        if q.lower() not in asked:
            return q
    return "That concludes the interview."

def generate_feedback(role, history):
    if not history:
        return "No answers recorded, cannot provide feedback."

    transcript = "\n".join(f"Q: {q}\nA: {a}" for q, a in history)

    prompt = f"""
You are a hiring manager evaluating a mock interview for a {role}.
Here is the candidate's interview transcript:

{transcript}

Give feedback that is:
- Carefully consider the mock interview question that was given (and an ideal response)
- Carefully consider the candidate's response to the question (provide feedback based on how they responded)
- Honest and specific to the candidate's answers in respect to the role
- Identify strengths and weaknesses
- Provide actionable advice for improvement
- End with an overall assessment

"""

    try:
        response = co.chat(
            model=MODEL,
            message=prompt,
            temperature=0.4,
            max_tokens=450,
        )

        feedback = response.text.strip()
        if feedback:
            return feedback
        else:
            return "The candidate's answers were recorded, but the AI could not generate specific feedback."

    except Exception as e:
        # Only fallback if API fails
        print(f"[FEEDBACK ERROR] {e}")
        return "The candidate's answers were recorded, but detailed AI feedback could not be generated at this time."










def analyze_resume(resume_text):
    prompt = f"""
You are a professional recruiter reviewing a resume.

Here is the resume text:
{resume_text}

Provide:
- Key strengths
- Areas for improvement
- Missing skills or experience
- Actionable suggestions to improve this resume

Be specific and constructive.
"""

    try:
        response = co.generate(
            model=MODEL,
            prompt=prompt,
            temperature=0.4,
            max_tokens=350,
        )

        return response.generations[0].text.strip()

    except Exception as e:
        print("[RESUME AI ERROR]", e, flush=True)
        return (
            "Your resume shows solid experience, but it would benefit from "
            "more quantified achievements and clearer impact statements."
        )


def analyze_resume(resume_text: str):
    """
    Generates actionable tips and a score for a resume text.
    Returns a dict structured for the frontend resume page.
    """
    prompt = f"""
You are an expert career coach. Here is a resume's content:

{resume_text}

Provide:
1. An overall score out of 10.
2. Feedback and actionable tips for each section:
   - Header / Contact Info
   - Objective / Summary
   - Work Experience
   - Skills
   - Education / Coursework
   - Structure & Formatting

Respond in JSON format like this:
{{
  "overall_score": "8",
  "tips": {{
    "header": {{"tip": "...", "score": "8"}},
    "objective": {{"tip": "...", "score": "7"}},
    "experience": {{"tip": "...", "score": "8"}},
    "skills": {{"tip": "...", "score": "7"}},
    "education": {{"tip": "...", "score": "8"}},
    "structure": {{"tip": "...", "score": "7"}}
  }}
}}
Respond ONLY in JSON.
"""

    import json

    for attempt in range(3):
        try:
            response = co.chat(
                model=MODEL,
                message=prompt,
                max_tokens=450,
                temperature=0.6,
            )

            text = response.text.strip()
            data = json.loads(text)
            return data

        except Exception as e:
            print(f"Cohere resume analysis error (attempt {attempt+1}):", e)
            time.sleep(0.5)

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
