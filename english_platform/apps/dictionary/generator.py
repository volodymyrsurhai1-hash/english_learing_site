import logging
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from apps.core.ai import get_llm_provider
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


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
    name: str = Field(
        description="Название слота без скобок, например: 'feature' или 'target'"
    )
    grammatical_form: Optional[str] = Field(
        default=None,
        description="Грамматическая форма: 'существительное / V-ing', 'прилагательное', 'инфинитив' и т.д.",
    )
    description: str = Field(
        description="Описание роли, что именно подставляется по смыслу (черта, физический объект, адресат и т.д.)"
    )
    examples: list[str] = Field(
        description="Список примеров подходящих слов или коротких фраз для этого слота: ['curiosity', 'patience']"
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
        default=None,
        description=(
            "Частотность слова в реальном современном английском языке по шкале от 1/10 до 10/10 "
            "с краткой характеристикой, например: '9/10 (Очень частое)', '7/10 (Распространённое)', "
            "'5/10 (Средняя частотность)', '2/10 (Редкое)'"
        ),
    )
    style: Optional[str] = Field(
        default=None,
        description=(
            "Стиль, регистр и сфера употребления слова или выражения: "
            "'Разговорный (неформальный)', 'Уличный сленг', 'Нейтральный (общеупотребительный)', "
            "'Литературный / Книжный', 'Газетный / Публицистический', 'Научный / Академический', "
            "'Официально-деловой', 'Профессиональный жаргон', 'Устаревший / Архаизм'. "
            "Если есть специфика сферы (например: медицина, IT, юриспруденция, спорт) — укажи её."
        ),
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
        default=None,
        description="Полная формула конструкции со слотами, например: '[feature] + be characteristic of + [group]'",
    )
    grammar_note: Optional[str] = Field(
        default=None,
        description="Особенность употребления или типичная ошибка (например, о предлоге, форме глагола или порядке слов)",
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


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True,
)
def analyze(query: str) -> LinguisticAnalysis:
    provider = get_llm_provider()
    prompt: str = f"""
Проанализируй английское слово или выражение: "{query}".
Определи: это отдельное слово ('word') или конструкция/фразовый глагол/идиома ('construction').

Обязательно определи:
1. Частотность слова (frequency) по шкале от 1/10 до 10/10 с краткой характеристикой частоты.
2. Точный стиль, регистр и сферу употребления (style): например, 'Разговорный (неформальный)', 'Уличный сленг', 'Нейтральный (общеупотребительный)', 'Литературный / Книжный', 'Газетный / Публицистический', 'Научный / Академический', 'Официально-деловой' или профессиональный жаргон.

Ключевые требования:
- Если это слово ('word') — ОБЯЗАТЕЛЬНО заполни поле meanings (все его значения с примерами), а также прямое определение на английском (english_definition), синонимы по уровням CEFR, популярные словосочетания (collocations) и семейство слов (word_family).
- Если конструкция ('construction') — ОБЯЗАТЕЛЬНО заполни:
  1. pattern: полную формулу конструкции со слотами в скобках (например, "[feature] + be characteristic of + [group]").
  2. slots: строго только внешние переменные части (placeholders). Сами слова и предлоги конструкции (например, 'characteristic' или 'of') НИКОГДА не выносятся в слоты! Для каждого слота укажи имя, грамматическую форму (grammatical_form), описание роли (description) и 3-5 конкретных слов-примеров (examples).
  3. grammar_note: полезная подсказка об особенностях употребления или типичной ошибке (например, о предлоге, согласовании или порядке слов).
  4. what_it_means: суть всей конструкции в целом.
  5. uses: применения конструкции с 2-3 живыми примерами полных предложений с переводом на русский.
  6. variations: если есть допустимые вариации порядка слов или синтаксиса.
К каждому значению/применению добавь по 2-3 живых примера на английском с качественным русским переводом.
"""
    return provider.generate_structured(prompt, LinguisticAnalysis)


def generate_and_export_dict(query: str) -> dict[str, Any]:
    analysis: LinguisticAnalysis = analyze(query)
    return analysis.model_dump()
