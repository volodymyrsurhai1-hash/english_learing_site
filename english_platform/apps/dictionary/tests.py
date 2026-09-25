from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.dictionary.generator import LinguisticAnalysis, analyze


class DictionaryGeneratorTests(SimpleTestCase):
    @patch("apps.dictionary.generator.get_llm_provider")
    def test_analyze_delegates_to_provider(self, mock_get_provider: MagicMock) -> None:
        mock_provider: MagicMock = MagicMock()
        mock_analysis: LinguisticAnalysis = LinguisticAnalysis(
            is_valid=True,
            entry_type="word",
            english="run",
            meanings=[],
        )
        mock_provider.generate_structured.return_value = mock_analysis
        mock_get_provider.return_value = mock_provider

        result: LinguisticAnalysis = analyze("run")

        self.assertEqual(result.english, "run")
        self.assertTrue(result.is_valid)
        mock_provider.generate_structured.assert_called_once()
