from functools import lru_cache

from django.conf import settings
from google import genai


@lru_cache(maxsize=1)
def get_ai_client() -> genai.Client:
    return genai.Client(api_key=settings.GEMINI_API_KEY)
