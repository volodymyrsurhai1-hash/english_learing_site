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


class DictionaryPresenterTests(SimpleTestCase):
    def test_present_deduplicates_redundant_pattern_and_essence(self) -> None:
        from apps.dictionary.presenters import (
            CuratedDictionaryEntry,
            DictionaryPresenter,
        )

        data = {
            "english": "regarding your feedback",
            "entry_type": "construction",
            "pattern": "regarding your feedback",
            "what_it_means": "Используется для обратной связи.",
            "uses": [
                {
                    "ru": "Используется для обратной связи.",
                    "examples": [
                        {
                            "en": "Regarding your feedback, we fixed it.",
                            "ru": "По поводу вашего отзыва, мы исправили.",
                        },
                        {
                            "en": "Regarding your feedback, thank you.",
                            "ru": "Спасибо за ваш отзыв.",
                        },
                        {
                            "en": "Regarding your feedback, we will proceed.",
                            "ru": "По поводу вашего отзыва, продолжим.",
                        },
                    ],
                }
            ],
            "slots": [
                {
                    "name": "feedback",
                    "description": "Тема или комментарий",
                    "examples": [
                        "your comments",
                        "Regarding your feedback, we improved our system.",
                    ],
                }
            ],
        }

        entry: CuratedDictionaryEntry = DictionaryPresenter.present(
            data, "regarding your feedback"
        )

        self.assertIsNone(entry.pattern)
        self.assertIsNone(entry.what_it_means)
        self.assertEqual(entry.primary_translation, "Используется для обратной связи.")
        self.assertEqual(len(entry.senses), 1)
        self.assertFalse(entry.senses[0].show_header)
        self.assertEqual(len(entry.senses[0].examples), 2)
        self.assertEqual(len(entry.slots), 1)
        self.assertEqual(entry.slots[0].tokens, ["your comments"])
        self.assertEqual(
            entry.slots[0].sentences,
            ["Regarding your feedback, we improved our system."],
        )

    def test_present_handles_construction_formula_and_grammar_notes(self) -> None:
        from apps.dictionary.presenters import (
            CuratedDictionaryEntry,
            DictionaryPresenter,
        )

        data = {
            "english": "characteristic of",
            "entry_type": "construction",
            "pattern": "[feature] + be characteristic of + [group]",
            "grammar_note": "Используется предлог of (не for). Глагол be изменяется по временам.",
            "what_it_means": "быть свойственным, характерным",
            "uses": [
                {
                    "ru": "быть свойственным для кого-то/чего-то",
                    "examples": [
                        {
                            "en": "Curiosity is characteristic of children.",
                            "ru": "Любопытство характерно для детей.",
                        }
                    ],
                }
            ],
            "slots": [
                {
                    "name": "[feature]",
                    "grammatical_form": "Существительное / V-ing",
                    "description": "Черта или свойство",
                    "examples": ["curiosity", "patience"],
                },
                {
                    "name": "group",
                    "grammatical_form": "Существительное",
                    "description": "Обладатель свойства",
                    "examples": ["children", "this species"],
                },
            ],
            "variations": [
                {
                    "pattern": "It is characteristic of [someone] to [do something]",
                    "note": "С инфинитивом",
                }
            ],
        }

        entry: CuratedDictionaryEntry = DictionaryPresenter.present(
            data, "characteristic of"
        )

        self.assertEqual(entry.pattern, "[feature] + be characteristic of + [group]")
        self.assertEqual(
            entry.grammar_note,
            "Используется предлог of (не for). Глагол be изменяется по временам.",
        )
        self.assertEqual(len(entry.slots), 2)
        self.assertEqual(entry.slots[0].name, "feature")
        self.assertEqual(entry.slots[0].grammatical_form, "Существительное / V-ing")
        self.assertEqual(entry.slots[0].tokens, ["curiosity", "patience"])
        self.assertEqual(entry.slots[1].name, "group")
        self.assertEqual(entry.slots[1].grammatical_form, "Существительное")
        self.assertEqual(len(entry.variations), 1)
        self.assertEqual(
            entry.variations[0].pattern,
            "It is characteristic of [someone] to [do something]",
        )
