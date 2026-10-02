from typing import Any, Optional

from django.core.management.base import BaseCommand

from apps.dictionary.generator import generate_and_export_dict
from apps.dictionary.models import Word


class Command(BaseCommand):
    help = "Purge or refresh cached words from the database so they can be regenerated cleanly."

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "words",
            nargs="+",
            type=str,
            help="One or more words to purge or refresh.",
        )
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Force regeneration of full_translation without deleting the word object.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        words: list[str] = options["words"]
        force_refresh: bool = options["refresh"]
        for raw_word in words:
            normalized: str = raw_word.lower().strip()
            word_obj: Optional[Word] = Word.objects.filter(word=normalized).first()
            if word_obj is None:
                self.stdout.write(
                    self.style.WARNING(
                        f"Word '{normalized}' was not found in database."
                    )
                )
                continue

            has_user_words: bool = word_obj.userword_set.exists()
            if force_refresh or has_user_words:
                new_data: dict[str, Any] = generate_and_export_dict(normalized)
                word_obj.full_translation = new_data
                word_obj.save(update_fields=["full_translation"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully refreshed '{normalized}' (preserved user links)."
                    )
                )
            else:
                word_obj.delete()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully deleted '{normalized}' from database."
                    )
                )
