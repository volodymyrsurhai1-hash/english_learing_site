import logging
from typing import Any, Optional

from apps.dictionary.generator import generate_and_export_dict
from apps.dictionary.models import Word

logger = logging.getLogger(__name__)


def get_or_generate_word(query: str) -> dict[str, Any]:
    normalized: str = query.lower().strip()

    word: Optional[Word] = Word.objects.filter(word=normalized).first()
    if word is not None:
        return word.full_translation

    result: dict[str, Any] = generate_and_export_dict(normalized)
    if not result:
        return {}

    word_instance, _ = Word.objects.get_or_create(
        word=normalized,
        defaults={"full_translation": result},
    )
    logger.info("Saved new word to DB: %s", normalized)

    return word_instance.full_translation
