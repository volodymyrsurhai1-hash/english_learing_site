from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings
from pydantic import BaseModel

from apps.core.ai import (
    GeminiProvider,
    LLMProvider,
    OpenAIProvider,
    get_llm_provider,
)


class DummySchema(BaseModel):
    name: str


class LLMProviderTests(SimpleTestCase):
    @override_settings(
        AI_PROVIDER="openai",
        OPENAI_API_KEY="test-key",
        OPENAI_MODEL="gpt-4o-mini",
    )
    def test_get_llm_provider_returns_openai(self) -> None:
        get_llm_provider.cache_clear()
        provider: LLMProvider = get_llm_provider()
        self.assertIsInstance(provider, OpenAIProvider)

    @override_settings(
        AI_PROVIDER="gemini",
        GEMINI_API_KEY="test-key",
        GEMINI_MODEL="gemini-3.6-flash",
    )
    def test_get_llm_provider_returns_gemini(self) -> None:
        get_llm_provider.cache_clear()
        provider: LLMProvider = get_llm_provider()
        self.assertIsInstance(provider, GeminiProvider)

    @override_settings(AI_PROVIDER="invalid")
    def test_get_llm_provider_raises_for_unsupported(self) -> None:
        get_llm_provider.cache_clear()
        with self.assertRaises(ValueError):
            get_llm_provider()

    @patch("apps.core.ai.OpenAI")
    def test_openai_provider_generate_structured(
        self, mock_openai_cls: MagicMock
    ) -> None:
        mock_client: MagicMock = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_completion: MagicMock = MagicMock()
        expected: DummySchema = DummySchema(name="test")
        mock_completion.choices = [MagicMock(message=MagicMock(parsed=expected))]
        mock_client.beta.chat.completions.parse.return_value = mock_completion

        provider: OpenAIProvider = OpenAIProvider(
            api_key="test-key", model="gpt-4o-mini"
        )
        result: DummySchema = provider.generate_structured("test prompt", DummySchema)

        self.assertEqual(result.name, "test")
        mock_client.beta.chat.completions.parse.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test prompt"}],
            response_format=DummySchema,
        )
