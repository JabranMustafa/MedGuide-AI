import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AIResponseGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing from .env file")

        self.client = OpenAI(api_key=api_key)

    def generate_response(self, user_message: str, symptoms, severity, duration, urgency: str) -> str:
        prompt = f"""
You are MedGuide AI, an educational medical assistant.

Rules:
- You are not a doctor.
- Do not diagnose.
- Do not prescribe medication.
- Do not claim certainty.
- Use simple language.
- If urgency is HIGH or EMERGENCY, recommend urgent medical care.

User message:
{user_message}

Extracted information:
Symptoms: {symptoms}
Severity: {severity}
Duration: {duration}
Urgency: {urgency}

Write a short, safe response.
"""

        try:
            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )

            return response.output_text

        except Exception as error:
            return (
                "AI response generation failed. "
                f"Technical error: {str(error)}"
            )