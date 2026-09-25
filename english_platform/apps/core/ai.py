import logging
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import TypeVar, cast

from django.conf import settings
from google import genai
from google.genai import types
from openai import OpenAI
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    @abstractmethod
    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._client: OpenAI = OpenAI(api_key=api_key)
        self._model: str = model

    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        logger.info(
            "Requesting structured completion from OpenAI model '%s'", self._model
        )
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            response_format=schema,
        )
        parsed: T | None = completion.choices[0].message.parsed
        if parsed is None:
            logger.error(
                "OpenAI model '%s' failed to parse structured output", self._model
            )
            raise ValueError("Failed to parse structured output from OpenAI response")
        logger.info(
            "Successfully received structured response from OpenAI model '%s'",
            self._model,
        )
        return parsed


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._client: genai.Client = genai.Client(api_key=api_key)
        self._model: str = model

    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        logger.info("Requesting structured content from Gemini model '%s'", self._model)
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            ),
        )
        logger.info(
            "Successfully received structured response from Gemini model '%s'",
            self._model,
        )
        if isinstance(response.parsed, schema):
            return response.parsed
        return cast(T, response.parsed)


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    provider_name: str = getattr(settings, "AI_PROVIDER", "openai").lower()
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=getattr(settings, "OPENAI_API_KEY", ""),
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
        )
    if provider_name == "gemini":
        return GeminiProvider(
            api_key=getattr(settings, "GEMINI_API_KEY", ""),
            model=getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash"),
        )
    raise ValueError(f"Unsupported AI provider: {provider_name}")


@lru_cache(maxsize=1)
def get_ai_client() -> genai.Client:
    return genai.Client(api_key=settings.GEMINI_API_KEY)
