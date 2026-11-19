import os

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the local .env file.
load_dotenv()


def get_setting(name: str, default: str | None = None) -> str | None:
    """
    Retrieve a configuration value.

    Priority:
    1. Environment variables (.env or system environment).
    2. Streamlit secrets (deployment configuration).
    3. Default value.
    """

    # Check environment variables first.
    value = os.getenv(name)

    if value:
        return value

    # Fall back to Streamlit secrets.
    try:
        return st.secrets[name]

    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        return default


# Retrieve Gemini configuration.
GEMINI_API_KEY = get_setting("GEMINI_API_KEY")
GEMINI_MODEL = get_setting(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)


# Validate required configuration.
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Configure it in your local .env file "
        "or Streamlit deployment secrets."
    )
