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
    ru: str = Field(
        description="Краткий прямой русский перевод конкретного значения (НЕ целое предложение, НЕ пример, без точки на конце)"
    )
    context: Optional[str] = Field(
        default=None,
        description="Часть речи и оттенок смысла, например: 'глагол: иметь значение', 'прилагательное: злой, подлый', 'существительное: среднее арифметическое'",
    )
    examples: list[Example] = Field(description="2-3 примера именно для этого значения")


class ConstructionSlot(BaseModel):
    name: str = Field(
        description="Название слота без скобок, например: 'subject' или 'place'"
    )
    grammatical_form: Optional[str] = Field(
        default=None,
        description="Грамматическая форма: 'существительное / местоимение', 'предлог + существительное', 'глагол V-ing' и т.д.",
    )
    description: str = Field(
        description="Описание роли, что именно подставляется по смыслу"
    )
    tokens: list[str] = Field(
        default_factory=list,
        description="3-5 конкретных подходящих слов или коротких фраз для подстановки в этот слот: ['the children', 'my roommate']",
    )
    examples: list[Example] = Field(
        default_factory=list,
        description="1-2 живых примера полных предложений с переводом, показывающих этот конкретный слот в действии внутри конструкции",
    )


class ConstructionUse(BaseModel):
    ru: str = Field(
        description="Краткий прямой русский перевод фразы или применения в этом контексте (НЕ предложение, НЕ пример, без точки на конце)"
    )
    context: Optional[str] = Field(
        default=None,
        description="Контекст употребления (прямое действие, переносный смысл и т.д.)",
    )
    examples: list[Example] = Field(description="2-3 примера употребления")


class Variation(BaseModel):
    pattern: str = Field(
        description="Вариация схемы со всеми необходимыми связками и предлогами, например: '[place] + be + a mess'"
    )
    note: str = Field(description="Пояснение, когда используется эта вариация")
    example: Optional[Example] = Field(
        default=None,
        description="Живой пример предложения с переводом, наглядно демонстрирующий эту вариацию схемы",
    )


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
            "(например, опечатка, случайный набор букв, слово из другого языка, бессмыслица). "
            "Если есть опечатка, укажи правильный вариант в suggested_correction. "
            "true — для любого реально существующего английского слова, фразы или идиомы."
        )
    )
    suggested_correction: Optional[str] = Field(
        default=None,
        description=(
            "Если запрос содержит опечатку или ошибку в написании (например, 'meen' -> 'mean', "
            "'definately' -> 'definitely'), укажи правильное написание базового слова или фразы, "
            "а is_valid установи в false. Если опечатки нет, оставь null."
        ),
    )
    entry_type: Literal["word", "construction"] = Field(
        description="Тип: 'word' для одиночных слов, 'construction' для фразовых глаголов, идиом и устойчивых конструкций"
    )
    english: str = Field(description="Слово или конструкция в базовой словарной форме")
    primary_translation: str = Field(
        default="",
        description=(
            "Строго прямой краткий словарный перевод слова или выражения на русский язык "
            "(1-3 точных слова/синонима через запятую, в той же части речи и грамматической форме; "
            "НЕ целое предложение, НЕ пример, НЕ объяснение сути, без точек на конце). "
            "Например: для 'mad skills' -> 'выдающиеся навыки, мастерство'; "
            "для 'mean' -> 'означать; злой; среднее значение'"
        ),
    )
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
        default=None,
        description=(
            "Часть речи на русском (например: 'глагол', 'существительное', 'прилагательное'). "
            "Если слово может быть разными частями речи (например, mean — глагол, прилагательное и существительное), "
            "перечисли все основные части речи через запятую."
        ),
    )
    collocations: list[str] = Field(
        default_factory=list, description="Популярные словосочетания в речи"
    )
    meanings: list[WordMeaning] = Field(
        default_factory=list,
        description=(
            "ВСЕ основные общеупотребительные значения слова с примерами. "
            "ОБЯЗАТЕЛЬНО охвати ВСЕ части речи слова, если их несколько (например, для mean: глагол 'означать/намереваться', "
            "прилагательное 'злой/скупой', существительное 'среднее значение')."
        ),
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
        default=None,
        description="Краткая суть/определение конструкции на русском (объяснение)",
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

КРИТИЧЕСКИ ВАЖНЫЕ ПРАВИЛА:
1. Валидация и опечатки:
   - Если запрос содержит опечатку или ошибку (например, "meen" вместо "mean", "definately" вместо "definitely", "recive" вместо "receive"):
     Установи is_valid=false и укажи правильное написание в suggested_correction (например, "mean"). Никакие словарные статьи для опечаток генерировать НЕЛЬЗЯ.
   - Если запрос не является английским словом или фразой (бессмыслица, случайный набор букв): установи is_valid=false, suggested_correction=null.
   - Если слово или выражение реально существует в английском языке: is_valid=true.

2. Прямой перевод (primary_translation и ru в значениях):
   - primary_translation — это СТРОГО краткий словарный перевод (1-3 точных слова/синонима, отвечающих на тот же грамматический вопрос, что и заголовок; БЕЗ точки на конце).
   - КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО писать в перевод полные предложения, примеры или описательные объяснения сути.
   - Для 'mad skills' прямой перевод — "выдающиеся навыки, мастерство" (а НЕ "У него крутые навыки в IT").
   - Для 'mean' прямой перевод — "означать; злой; среднее значение".
   - Объяснение сути пиши только в what_it_means или english_definition, но НЕ в переводе.

3. Многозначность и части речи:
   - Если слово может выступать разными частями речи (например, mean: глагол, прилагательное, существительное; run: глагол, существительное):
     В поле part_of_speech перечисли ВСЕ эти части речи через запятую.
     В списке meanings ОБЯЗАТЕЛЬНО приведи ВСЕ ключевые общеупотребительные значения для КАЖДОЙ части речи, от наиболее частых к менее частым.
     В поле context каждого значения обязательно укажи часть речи и смысловой оттенок (например: "глагол: означать", "глагол: намереваться", "прилагательное: злой, грубый", "прилагательное: скупой", "существительное: среднее арифметическое").

4. Конструкции и идиомы:
   - Если это конструкция или идиома ('construction'):
     1. pattern: полная, грамматически точная формула конструкции со слотами в квадратных скобках.
        СХЕМА ОБЯЗАНА ВКЛЮЧАТЬ ВСЕ НЕОБХОДИМЫЕ ПРЕДЛОГИ И СВЯЗКИ!
        КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО пропускать предлоги: не '[subject] + make + a mess + [object]' (так как 'make a mess the kitchen' — грубая ошибка), а '[subject] + make a mess + (in [place] / of [thing])' или '[subject] + make a mess + in [place]'.
     2. slots: строго только внешние переменные части (placeholders). Сами фиксированные слова конструкции НИКОГДА не выносятся в слоты!
        Для каждого слота ОБЯЗАТЕЛЬНО заполни:
        - name: имя слота без скобок ('subject', 'place', 'target');
        - grammatical_form: форма ('существительное / местоимение', 'предлог + существительное', 'V-ing');
        - description: точная смысловая роль;
        - tokens: 3-5 конкретных слов/фраз для подстановки (например: ['the children', 'my roommate', 'someone']);
        - examples: 1-2 живых примера полных предложений с переводом (en, ru), наглядно показывающих использование именно этого слота в конструкции.
     3. grammar_note: полезная подсказка об особенностях употребления (предлоги, форма глагола, порядок слов).
     4. what_it_means: подробное объяснение сути конструкции на русском.
     5. uses: применения конструкции с кратким прямым русским переводом (ru) и 2-3 живыми примерами с переводом.
     6. variations: если допустимы вариации схемы. Для каждой вариации обязательно укажи формулу (pattern), пояснение (note) и живой пример с переводом (example: en, ru).

Обязательно определи частотность (frequency) от 1/10 до 10/10 и точный стиль/сферу (style).
К каждому значению добавь по 2-3 живых примера на английском с качественным русским переводом.
"""
    return provider.generate_structured(prompt, LinguisticAnalysis)


def generate_and_export_dict(query: str) -> dict[str, Any]:
    analysis: LinguisticAnalysis = analyze(query)
    return analysis.model_dump()
