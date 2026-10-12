import random

from apps.dictionary.models import UserWord


class DeckService:
    @staticmethod
    def get_or_create_deck(session, user) -> list[int]:
        if not session.get("card_deck", 0):
            words = UserWord.objects.filter(user=user, status="LEARNING").values_list(
                "pk", flat=True
            )
            list_words = list(words)
            random.shuffle(list_words)
            session["card_deck"] = list_words
            session.modified = True
            return session["card_deck"]
        return session.get("card_deck", [])

    @staticmethod
    def get_next_pk(session, current_pk: int):
        deck: list[int] = session.get("card_deck", [])
        if not deck:
            return None

        try:
            current_index = deck.index(current_pk)
            if current_index + 1 < len(deck):
                return deck[current_index + 1]
        except ValueError:
            return deck[0]

        return None

    @staticmethod
    def remove_pk(session, pk: int):
        deck = session.get("card_deck", [])

        if pk in deck:
            deck.remove(pk)
            session.modified = True

    @staticmethod
    def add_pk(session, pk: int) -> None:
        deck = session.get("card_deck")
        if deck is not None and pk not in deck:
            deck.insert(0, pk)
            session.modified = True
