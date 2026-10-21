import random
from typing import Optional

from django.core.cache import cache

from apps.dictionary.models import UserWord


class DeckService:
    DECK_TIMEOUT: int = 60 * 60 * 24

    @classmethod
    def _get_cache_key(cls, user) -> str:
        return f"deck:user:{user.pk}"

    @classmethod
    def get_or_create_deck(cls, user) -> list[int]:
        cache_key = cls._get_cache_key(user)
        deck: list[int] | None = cache.get(cache_key)
        if not deck:
            words = UserWord.objects.filter(user=user, status="LEARNING").values_list(
                "pk", flat=True
            )
            deck = list(words)
            random.shuffle(deck)
            cache.set(cache_key, deck, timeout=cls.DECK_TIMEOUT)
        return deck

    @classmethod
    def get_next_pk(cls, user, current_pk: int) -> Optional[int]:
        cache_key = cls._get_cache_key(user)
        deck: list[int] = cache.get(cache_key) or []

        if not deck:
            return None

        try:
            current_index = deck.index(current_pk)
            if current_index + 1 < len(deck):
                return deck[current_index + 1]
        except ValueError:
            return deck[0]

        return None

    @classmethod
    def remove_pk(cls, user, pk: int) -> None:
        cache_key = cls._get_cache_key(user)
        deck: list[int] | None = cache.get(cache_key)

        if deck and pk in deck:
            deck.remove(pk)
            cache.set(cache_key, deck, timeout=cls.DECK_TIMEOUT)

    @classmethod
    def add_pk(cls, user, pk: int) -> None:
        cache_key = cls._get_cache_key(user)
        deck: list[int] | None = cache.get(cache_key)

        if deck is not None and pk not in deck:
            deck.insert(0, pk)
            cache.set(cache_key, deck, timeout=cls.DECK_TIMEOUT)
