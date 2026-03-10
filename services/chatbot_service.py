import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def chatbot_response(msg):

    prompt=f"""
You are an AI Insurance Assistant.

Help users understand:
insurance claims
fraud detection
policy eligibility
documents required

User question: {msg}
"""

    model=genai.GenerativeModel("gemini-2.5-flash")

    response=model.generate_content(prompt)

    return response.text