import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-pro"
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        prompt = f"""
You are a legal document drafting assistant.

Create a professional draft of the following legal document.

Document Type:
{document_type}

Parties:
{parties}

Effective Date / Dates:
{dates}

Terms and Conditions:
{terms}

Requirements:
- Use clear professional legal language.
- Include appropriate headings and sections.
- Organize the document clearly.
- Do not invent important facts that were not provided.
- Return only the document text.
- Add a short notice at the end that this is an AI-generated draft
  and should be reviewed by a qualified legal professional.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text