import logging
import re
from typing import Any, Optional

from apps.dictionary.generator import generate_and_export_dict
from apps.dictionary.models import UserWord, Word

logger = logging.getLogger(__name__)


class WordNotFoundError(Exception):
    pass


class AIServiceUnavailableError(Exception):
    pass


def validate_query(query: str) -> Optional[str]:
    if not query:
        return "Введите слово или выражение."
    if len(query) > 100:
        return "Запрос слишком длинный. Максимум — 100 символов."
    if not re.search(r"[a-zA-Z]", query):
        return "Запрос должен содержать английские буквы."
    return None


def get_or_generate_word(query: str) -> dict[str, Any]:
    normalized: str = query.lower().strip()

    word: Optional[Word] = Word.objects.filter(word=normalized).first()
    if word is not None:
        return word.full_translation

    try:
        result: dict[str, Any] = generate_and_export_dict(normalized)
    except Exception as exc:
        logger.error("AI generation failed after retries for %s: %s", normalized, exc)
        raise AIServiceUnavailableError(
            "Сервис генерации временно перегружен. Пожалуйста, попробуйте еще раз через несколько секунд."
        ) from exc

    if not result.get("is_valid", True):
        raise WordNotFoundError(
            f"«{query}» не является существующим английским словом или выражением."
        )

    word_instance, _ = Word.objects.get_or_create(
        word=normalized,
        defaults={"full_translation": result},
    )
    logger.info("Saved new word to DB: %s", normalized)

    return word_instance.full_translation


def save_word_for_user(word_text: str, user: Any) -> tuple[UserWord, bool]:
    normalized: str = word_text.lower().strip()
    word: Optional[Word] = Word.objects.filter(word=normalized).first()
    if word is None:
        raise Word.DoesNotExist(f"Word '{normalized}' not found in DB.")
    user_word, created = UserWord.objects.get_or_create(user=user, word=word)
    return user_word, created


def delete_word_for_user(word_text: str, user: Any) -> None:
    normalized: str = word_text.lower().strip()
    UserWord.objects.filter(user=user, word__word=normalized).delete()


def is_word_saved(word_text: str, user: Any) -> bool:
    normalized: str = word_text.lower().strip()
    return UserWord.objects.filter(user=user, word__word=normalized).exists()


def toggle_word_status(word_text: str, user: Any) -> None:
    normalized: str = word_text.lower().strip()
    user_word: Optional[UserWord] = UserWord.objects.filter(
        user=user, word__word=normalized
    ).first()
    if user_word is None:
        return
    if user_word.status == "LEARNING":
        user_word.status = "LEARNED"
    else:
        user_word.status = "LEARNING"
    user_word.save(update_fields=["status"])
