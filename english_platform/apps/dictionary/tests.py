from typing import Any
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.dictionary.generator import LinguisticAnalysis, analyze
from apps.dictionary.presenters import (
    CuratedDictionaryEntry,
    DictionaryPresenter,
)
from apps.dictionary.services import WordNotFoundError, get_or_generate_word


class DictionaryGeneratorTests(SimpleTestCase):
    @patch("apps.dictionary.generator.get_llm_provider")
    def test_analyze_delegates_to_provider(self, mock_get_provider: MagicMock) -> None:
        mock_provider: MagicMock = MagicMock()
        mock_analysis: LinguisticAnalysis = LinguisticAnalysis(
            is_valid=True,
            entry_type="word",
            english="mean",
            primary_translation="означать; злой; среднее значение",
            part_of_speech="глагол, прилагательное, существительное",
            meanings=[],
        )
        mock_provider.generate_structured.return_value = mock_analysis
        mock_get_provider.return_value = mock_provider

        result: LinguisticAnalysis = analyze("mean")

        self.assertEqual(result.english, "mean")
        self.assertTrue(result.is_valid)
        self.assertEqual(result.primary_translation, "означать; злой; среднее значение")
        mock_provider.generate_structured.assert_called_once()

    @patch("apps.dictionary.generator.get_llm_provider")
    def test_analyze_handles_typo_with_suggestion(
        self, mock_get_provider: MagicMock
    ) -> None:
        mock_provider: MagicMock = MagicMock()
        mock_analysis: LinguisticAnalysis = LinguisticAnalysis(
            is_valid=False,
            suggested_correction="mean",
            entry_type="word",
            english="meen",
            primary_translation="",
            meanings=[],
        )
        mock_provider.generate_structured.return_value = mock_analysis
        mock_get_provider.return_value = mock_provider

        result: LinguisticAnalysis = analyze("meen")

        self.assertFalse(result.is_valid)
        self.assertEqual(result.suggested_correction, "mean")


class DictionaryPresenterTests(SimpleTestCase):
    def test_present_prioritizes_explicit_primary_translation(self) -> None:
        data: dict[str, Any] = {
            "english": "mad skills",
            "entry_type": "construction",
            "primary_translation": "крутые навыки, мастерство.",
            "what_it_means": "Обозначает выдающиеся способности.",
            "uses": [
                {
                    "ru": "У него крутые навыки программирования.",
                    "examples": [
                        {
                            "en": "He has mad skills in python.",
                            "ru": "У него крутые навыки в python.",
                        }
                    ],
                }
            ],
        }

        entry: CuratedDictionaryEntry = DictionaryPresenter.present(data, "mad skills")

        self.assertEqual(entry.primary_translation, "крутые навыки, мастерство")

    def test_present_multi_senses_shows_headers(self) -> None:
        data: dict[str, Any] = {
            "english": "mean",
            "entry_type": "word",
            "primary_translation": "означать; злой; среднее значение",
            "part_of_speech": "глагол, прилагательное, существительное",
            "meanings": [
                {
                    "ru": "означать, иметь значение",
                    "context": "глагол",
                    "examples": [
                        {
                            "en": "What does this mean?",
                            "ru": "Что это означает?",
                        }
                    ],
                },
                {
                    "ru": "злой, недоброжелательный",
                    "context": "прилагательное",
                    "examples": [
                        {
                            "en": "Don't be mean.",
                            "ru": "Не будь злым.",
                        }
                    ],
                },
                {
                    "ru": "среднее арифметическое",
                    "context": "существительное",
                    "examples": [
                        {
                            "en": "Calculate the mean.",
                            "ru": "Посчитай среднее.",
                        }
                    ],
                },
            ],
        }

        entry: CuratedDictionaryEntry = DictionaryPresenter.present(data, "mean")

        self.assertEqual(entry.primary_translation, "означать; злой; среднее значение")
        self.assertEqual(len(entry.senses), 3)
        self.assertTrue(entry.senses[0].show_header)
        self.assertEqual(entry.senses[0].context, "глагол")
        self.assertTrue(entry.senses[1].show_header)
        self.assertEqual(entry.senses[1].context, "прилагательное")
        self.assertTrue(entry.senses[2].show_header)
        self.assertEqual(entry.senses[2].context, "существительное")

    def test_present_deduplicates_redundant_pattern_and_essence(self) -> None:
        data: dict[str, Any] = {
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
        data: dict[str, Any] = {
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


class DictionaryServiceTests(SimpleTestCase):
    @patch("apps.dictionary.services.Word.objects")
    @patch("apps.dictionary.services.generate_and_export_dict")
    def test_get_or_generate_word_raises_with_suggestion(
        self,
        mock_generate: MagicMock,
        mock_word_objects: MagicMock,
    ) -> None:
        mock_word_objects.filter.return_value.first.return_value = None
        mock_generate.return_value = {
            "is_valid": False,
            "suggested_correction": "mean",
        }

        with self.assertRaises(WordNotFoundError) as cm:
            get_or_generate_word("meen")

        self.assertEqual(cm.exception.suggestion, "mean")
        self.assertIn("«meen» не найдено в словаре", str(cm.exception))
        mock_word_objects.get_or_create.assert_not_called()

    @patch("apps.dictionary.services.Word.objects")
    @patch("apps.dictionary.services.generate_and_export_dict")
    def test_get_or_generate_word_saves_under_canonical_word(
        self,
        mock_generate: MagicMock,
        mock_word_objects: MagicMock,
    ) -> None:
        mock_word_objects.filter.return_value.first.return_value = None
        mock_instance: MagicMock = MagicMock()
        mock_instance.full_translation = {
            "english": "mean",
            "is_valid": True,
            "primary_translation": "означать",
        }
        mock_word_objects.get_or_create.return_value = (mock_instance, True)
        mock_generate.return_value = {
            "english": "mean",
            "is_valid": True,
            "primary_translation": "означать",
        }

        result: dict[str, Any] = get_or_generate_word("Mean")

        self.assertEqual(result["english"], "mean")
        mock_word_objects.get_or_create.assert_called_once_with(
            word="mean",
            defaults={
                "full_translation": {
                    "english": "mean",
                    "is_valid": True,
                    "primary_translation": "означать",
                }
            },
        )
