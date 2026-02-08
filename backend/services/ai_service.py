#all AI calls

import os
import cohere
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
Ask ONE new interview question. Do NOT repeat previous questions. Respond ONLY with the question text.
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










