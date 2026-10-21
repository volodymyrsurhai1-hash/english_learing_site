import random

from apps.dictionary.models import UserWord
from django.core.cache import cache
from typing import Optional


class DeckService:
    DECK_TIMEOUT = 60 * 60 * 24  # 1 day in seconds

    @staticmethod
    def _get_cache_key(user) -> str:
        return f"deck:user:{user.pk}"

    @staticmethod
    def get_or_create_deck(cls, user) -> list[int]:
        cache_key = cls._get_cache_key(user)
        deck = cache.get(cache_key)
        if not deck:
            words = UserWord.objects.filter(user=user, status="LEARNING").values_list(
                "pk", flat=True
            )
            deck = list(words)
            random.shuffle(deck)
            cache.set(cache_key, deck)
        return deck

    @classmethod
    def get_next_pk(cls, user, current_pk: int) -> Optional[int]:
        cache_key = cls._get_cache_key(user)
        deck = cache.get(cache_key) or []

        if not deck:
            return None

        try:
            current_index = deck.index(current_pk)
            if current_index + 1 < len(deck):
                return deck[current_index + 1]
        except ValueError:
            pass

        return deck[0]

    @classmethod
    def remove_pk(cls, user, pk: int) -> None:
        cache_key = cls._get_cache_key(user)
        deck = cache.get(cache_key)

        if deck and pk in deck:
            deck.remove(pk)
            cache.set(cache_key, deck, timeout=cls.DECK_TIMEOUT)

    @classmethod
    def add_pk(cls, user, pk: int) -> None:
        cache_key = cls._get_cache_key(user)
        deck = cache.get(cache_key)

        if deck is not None and pk not in deck:
            deck.insert(0, pk)
            cache.set(cache_key, deck, timeout=cls.DECK_TIMEOUT)
