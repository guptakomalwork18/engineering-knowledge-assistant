import unittest
from unittest.mock import patch

from app.services.gemini_service import (
    generate_response,
    GeminiServiceError,
)


class FakeGeminiError(Exception):
    """Simulates an error returned by Gemini."""

    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class TestGeminiServiceErrors(unittest.TestCase):

    @patch("app.services.gemini_service.client.interactions.create")
    def test_service_unavailable_error(self, mock_create):

        # Simulate Gemini returning HTTP 503.
        mock_create.side_effect = FakeGeminiError(
            "Error 503: Gemini is currently experiencing high demand.",
            503,
        )

        # Verify that our application converts the error.
        with self.assertRaises(GeminiServiceError) as context:
            generate_response("Explain Apache Kafka.")

        # Verify the error category.
        self.assertEqual(
            context.exception.category,
            "service_unavailable",
        )

        # Verify the user-friendly message.
        self.assertIn(
            "temporarily experiencing high demand",
            context.exception.user_message,
        )

        # Verify that the original error is preserved.
        self.assertIsNotNone(context.exception.__cause__)

        print("HTTP 503 error handling test passed!")

    @patch("app.services.gemini_service.client.interactions.create")
    def test_rate_limit_error(self, mock_create):

        mock_create.side_effect = FakeGeminiError(
            "Error 429: Too many requests.",
            429,
        )

        with self.assertRaises(GeminiServiceError) as context:
            generate_response("Explain Apache Kafka.")

        self.assertEqual(
            context.exception.category,
            "rate_limit",
        )

        print("HTTP 429 error handling test passed!")

    @patch("app.services.gemini_service.client.interactions.create")
    def test_timeout_error(self, mock_create):

        mock_create.side_effect = TimeoutError("Request timed out.")

        with self.assertRaises(GeminiServiceError) as context:
            generate_response("Explain Apache Kafka.")

        self.assertEqual(
            context.exception.category,
            "timeout",
        )

        print("Timeout error handling test passed!")


if __name__ == "__main__":
    unittest.main()
