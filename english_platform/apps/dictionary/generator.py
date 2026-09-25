import logging
from typing import Literal, Optional, cast

from django.conf import settings
from google.genai import types
from pydantic import BaseModel, Field

from apps.core.ai import get_ai_client
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

MODEL: str = getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")


# ── Схемы Pydantic ────────────────────────────────────


class Example(BaseModel):
    en: str = Field(description="Предложение на английском")
    ru: str = Field(description="Точный перевод на русский")
    tag: Optional[str] = Field(
        default=None,
        description="Тег: прямое значение / переносное значение / вопрос / отрицание / сленг",
    )


class WordMeaning(BaseModel):
    ru: str = Field(description="Русский перевод конкретного значения")
    context: Optional[str] = Field(
        default=None, description="Часть речи, область употребления или оттенок смысла"
    )
    examples: list[Example] = Field(description="2-3 примера именно для этого значения")


class ConstructionSlot(BaseModel):
    name: str = Field(description="Название слота, например: 'ЧТО' или 'КОГО'")
    description: str = Field(
        description="Описание, что именно подставляется (физические объекты, критика и т.д.)"
    )
    examples: list[str] = Field(
        description="Список примеров подходящих слов: ['dust', 'crumbs', 'criticism']"
    )


class ConstructionUse(BaseModel):
    ru: str = Field(description="Перевод этого применения или смысла")
    context: Optional[str] = Field(
        default=None,
        description="Контекст употребления (прямое действие, переносный смысл и т.д.)",
    )
    examples: list[Example] = Field(description="2-3 примера употребления")


class Variation(BaseModel):
    pattern: str = Field(description="Вариация схемы, например: 'brush off + что'")
    note: str = Field(description="Пояснение, когда используется эта вариация")


class SynonymGroup(BaseModel):
    level: str = Field(
        description="Уровень сложности синонимов (A1, A2, B1, B2, C1, C2)"
    )
    synonyms: list[str] = Field(
        description="Список синонимов, относящихся к этому уровню"
    )


class LinguisticAnalysis(BaseModel):
    is_valid: bool = Field(
        description=(
            "false — если запрос не является существующим английским словом или выражением "
            "(например, случайный набор букв, слово из другого языка, бессмыслица). "
            "Если is_valid=false, все остальные поля можно не заполнять. "
            "true — для любого реального английского слова, фразы или идиомы."
        )
    )
    entry_type: Literal["word", "construction"] = Field(
        description="Тип: 'word' для одиночных слов, 'construction' для фразовых глаголов, идиом и устойчивых конструкций"
    )
    english: str = Field(description="Слово или конструкция в базовой форме")
    cefr: Optional[str] = Field(
        default=None, description="Уровень сложности: A1, A2, B1, B2, C1, C2"
    )
    frequency: Optional[str] = Field(
        default=None, description="Частотность, например: '8/10'"
    )
    style: Optional[str] = Field(
        default=None,
        description="Стиль: Нейтральный / Разговорный / Формальный / Идиоматический",
    )

    transcription: Optional[str] = Field(
        default=None, description="Транскрипция, например: '/rʌn/'"
    )
    part_of_speech: Optional[str] = Field(
        default=None, description="Часть речи (существительное, глагол и т.д.)"
    )
    collocations: list[str] = Field(
        default_factory=list, description="Популярные словосочетания в речи"
    )
    meanings: list[WordMeaning] = Field(
        default_factory=list,
        description="ВСЕ значения слова с примерами. ОБЯЗАТЕЛЬНО ЗАПОЛНЯТЬ, если entry_type=='word'!",
    )
    english_definition: Optional[str] = Field(
        default=None, description="Прямое определение слова на английском языке"
    )
    synonyms_by_level: list[SynonymGroup] = Field(
        default_factory=list,
        description="Синонимы, сгруппированные по уровням сложности (CEFR)",
    )
    word_family: list[str] = Field(
        default_factory=list,
        description="Семейство слов (однокоренные слова от базового до производных), например: ['lovely', 'lover', 'loving', 'loved']",
    )

    pattern: Optional[str] = Field(
        default=None, description="Схема конструкции, например: 'brush + что + off'"
    )
    what_it_means: Optional[str] = Field(
        default=None, description="Краткая суть/определение конструкции"
    )
    slots: list[ConstructionSlot] = Field(
        default_factory=list, description="Слоты конструкции (что подставлять)"
    )
    uses: list[ConstructionUse] = Field(
        default_factory=list,
        description="ВСЕ применения и смыслы конструкции с примерами",
    )
    variations: list[Variation] = Field(
        default_factory=list, description="Вариации порядка слов"
    )


# ── Интерфейс ────────────────────────────────────


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True,
)
def analyze(query: str) -> LinguisticAnalysis:
    client = get_ai_client()

    prompt = f"""
Проанализируй английское слово или выражение: "{query}".
Определи: это отдельное слово ('word') или конструкция/фразовый глагол/идиома ('construction').
Это ОЧЕНЬ ВАЖНО:
- Если это слово ('word') — ОБЯЗАТЕЛЬНО заполни поле meanings (все его значения), а также прямое определение на английском, синонимы, и семейство слов.
- Если конструкция ('construction') — ОБЯЗАТЕЛЬНО заполни поле uses (все её применения) и слоты.
К каждому значению/применению добавь по 2-3 живых примера.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LinguisticAnalysis,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )
    if isinstance(response.parsed, LinguisticAnalysis):
        return response.parsed
    return cast(LinguisticAnalysis, response.parsed)


def generate_and_export_dict(query: str) -> dict:
    analysis = analyze(query)
    return analysis.model_dump()
