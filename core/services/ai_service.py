import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from core.exceptions import (AIQuotaExceededError,AIServiceUnavailableError,)
    


load_dotenv()


class AIService:
    """Handles AI content generation using Google Gemini."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-flash-latest"

    def generate(
    self,
    prompt: str,
    max_retries: int = 3,
    retry_delay: int = 3,
) -> str:
        """Generate content using Gemini with retry handling."""

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if not response or not response.text:
                    raise RuntimeError("Gemini returned an empty response.")

                return response.text.strip()

            except errors.ServerError as error:
                last_error = error

                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue

                raise AIServiceUnavailableError(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                ) from last_error

            except errors.ClientError as error:
                if getattr(error, "status_code", None) == 429:
                    raise AIQuotaExceededError(
                        "Gemini API quota exceeded. "
                        "Please check your Gemini API quota or billing plan."
                    ) from error

                raise RuntimeError(
                    f"Gemini API error: {error}"
                ) from error

        raise RuntimeError("Gemini generation failed.")

ai_service = AIService()

