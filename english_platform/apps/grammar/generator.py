import logging
from typing import Any, Literal, cast

from django.conf import settings
from google.genai import types
from pydantic import BaseModel, Field

from apps.core.ai import get_ai_client

logger = logging.getLogger(__name__)

MODEL: str = getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")


class Example(BaseModel):
    en: str = Field(description="Предложение на английском языке")
    ru: str = Field(description="Качественный и естественный русский перевод")
    note: str = Field(default="", description="Краткое пояснение к примеру")


class FormulaRow(BaseModel):
    subject: str = Field(description="Группа местоимений или подлежащее")
    affirmative: str = Field(description="Утвердительная форма с глаголом")
    negative: str = Field(description="Отрицательная форма")
    question: str = Field(description="Вопросительная форма")


class Scenario(BaseModel):
    title: str = Field(description="Краткое название случая употребления")
    description: str = Field(description="Понятное объяснение сути этого сценария")
    examples: list[Example] = Field(description="2-3 примера с переводом")


class ExerciseItem(BaseModel):
    question: str = Field(description="Предложение с пропуском или задание")
    answer: str = Field(description="Правильный ответ")


class Exercise(BaseModel):
    title: str = Field(description="Название упражнения")
    instruction: str = Field(description="Инструкция к выполнению задания")
    items: list[ExerciseItem] = Field(description="3-5 заданий для самопроверки")


class GrammarTopicAnalysis(BaseModel):
    is_valid: bool = Field(
        description="true если запрос является реальной темой английской грамматики, false если это бессмыслица или случайный набор символов"
    )
    slug: str = Field(description="URL-слаг в kebab-case")
    title: str = Field(description="Английское название темы")
    subtitle: str = Field(description="Русское название темы")
    category: Literal[
        "tenses", "conditionals", "modals", "non_finite", "reported", "advanced"
    ] = Field(
        description="Категория: tenses, conditionals, modals, non_finite, reported, advanced"
    )
    level: Literal["A1", "A2", "B1", "B2", "C1"] = Field(
        description="Уровень сложности по CEFR"
    )
    essence: str = Field(
        description="Краткая суть правила простыми словами, 2-3 предложения"
    )
    formulas: list[FormulaRow] = Field(
        description="Таблица формул утверждения, отрицания и вопроса"
    )
    formula_note: str = Field(
        default="", description="Важное примечание к образованию форм"
    )
    scenarios: list[Scenario] = Field(
        description="3-4 сценария употребления с описанием и примерами"
    )
    markers: list[str] = Field(
        default_factory=list, description="Слова-маркеры времени или сигнальные слова"
    )
    exercises: list[Exercise] = Field(
        default_factory=list, description="1-2 упражнения для закрепления темы"
    )


def generate_grammar_topic(query: str) -> GrammarTopicAnalysis:
    client = get_ai_client()

    prompt: str = f"""
Составь подробный, структурированный учебный конспект по английской грамматике для темы: "{query}".
Определи, является ли это реальным грамматическим правилом английского языка:
- Если нет (бессмыслица, опечатка, не грамматика) — верни is_valid=false.
- Если да — верни is_valid=true и заполни все поля конспекта.
Сделай объяснение максимально живым, доступным и понятным, с практическими примерами и формулами.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GrammarTopicAnalysis,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    if isinstance(response.parsed, GrammarTopicAnalysis):
        return response.parsed
    return cast(GrammarTopicAnalysis, response.parsed)


def generate_and_export_topic(query: str) -> dict[str, Any]:
    analysis: GrammarTopicAnalysis = generate_grammar_topic(query)
    return analysis.model_dump()
