from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.grammar.generator import GrammarTopicAnalysis, generate_grammar_topic


class GrammarGeneratorTests(SimpleTestCase):
    @patch("apps.grammar.generator.get_llm_provider")
    def test_generate_grammar_topic_delegates_to_provider(
        self, mock_get_provider: MagicMock
    ) -> None:
        mock_provider: MagicMock = MagicMock()
        mock_analysis: GrammarTopicAnalysis = GrammarTopicAnalysis(
            is_valid=True,
            slug="present-simple",
            title="Present Simple",
            subtitle="Простое настоящее время",
            category="tenses",
            level="A1",
            essence="Правило для регулярных действий.",
            formulas=[],
            formula_note="",
            scenarios=[],
            markers=[],
            exercises=[],
        )
        mock_provider.generate_structured.return_value = mock_analysis
        mock_get_provider.return_value = mock_provider

        result: GrammarTopicAnalysis = generate_grammar_topic("Present Simple")

        self.assertEqual(result.slug, "present-simple")
        self.assertTrue(result.is_valid)
        mock_provider.generate_structured.assert_called_once()
