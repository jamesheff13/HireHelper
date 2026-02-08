import json
from services.ai_service import co, MODEL

def analyze_linkedin(linkedin_text: str) -> dict:
    """
    Takes raw LinkedIn profile text and returns structured recommendations:
    headline, about, experience, connections, visual
    """

    # 🔹 TRUNCATE TEXT TO SAFE LENGTH
    MAX_LENGTH = 4000  # characters
    linkedin_text = linkedin_text[:MAX_LENGTH]
    
    prompt = f"""
You are a professional career coach analyzing a LinkedIn profile. Here is the profile text:

{linkedin_text}

Provide constructive, actionable tips for improving the profile. 
Respond in JSON format exactly like this:
{{
  "headline": "...",
  "about": "...",
  "experience": "...",
  "connections": "...",
  "visual": "..."
}}
Respond ONLY in JSON.
"""
    for attempt in range(3):
        try:
            response = co.chat(
                model=MODEL,
                message=prompt,
                temperature=0.6,
                max_tokens=450,
            )
            data = json.loads(response.text.strip())
            return data
        except Exception as e:
            print(f"[LinkedIn AI error attempt {attempt+1}]:", e)

    # fallback if AI fails
    return {
        "headline": "No suggestions available",
        "about": "No suggestions available",
        "experience": "No suggestions available",
        "connections": "No suggestions available",
        "visual": "No suggestions available",
    }