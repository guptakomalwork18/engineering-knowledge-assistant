
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiServiceError(Exception):
    """Represents a user-friendly Gemini service error."""

    def __init__(self, message: str, category: str):
        super().__init__(message)
        self.category = category
        self.user_message = message


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"timeout": 30000},
)


def generate_response(prompt: str) -> str:
    try:
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=prompt,
        )

        return interaction.output_text

    except Exception as error:
        error_code = str(getattr(error, "code", ""))
        error_message = str(error).lower()

        if (
            error_code == "503"
            or "503" in error_message
            or "high demand" in error_message
        ):
            raise GeminiServiceError(
                "Gemini is temporarily experiencing high demand. "
                "Please try again later.",
                category="service_unavailable",
            ) from error

        elif error_code == "429" or "429" in error_message:
            raise GeminiServiceError(
                "Gemini request limits have been reached. "
                "Please wait before trying again.",
                category="rate_limit",
            ) from error

        elif "timeout" in error_message or "timed out" in error_message:
            raise GeminiServiceError(
                "Gemini took too long to respond. "
                "Please try again later.",
                category="timeout",
            ) from error

        elif error_code in ("401", "403"):
            raise GeminiServiceError(
                "Gemini authentication failed. "
                "Please check the API configuration.",
                category="authentication",
            ) from error

        else:
            raise GeminiServiceError(
                "An unexpected error occurred while generating "
                "the answer. Please try again later.",
                category="unknown",
            ) from error
