
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_setting(key, default=None):
    """Read configuration from environment or Streamlit secrets."""

    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


OPENAI_API_KEY = get_setting("OPENAI_API_KEY")
OPENAI_MODEL = get_setting("OPENAI_MODEL", "gpt-4.1-mini")

TAVILY_API_KEY = get_setting("TAVILY_API_KEY")

RESEND_API_KEY = get_setting("RESEND_API_KEY")
RESEND_FROM_EMAIL = get_setting("RESEND_FROM_EMAIL")
