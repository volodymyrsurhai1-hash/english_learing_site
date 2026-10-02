from django.contrib import admin

from apps.dictionary.models import UserWord, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "get_primary_translation")
    search_fields = ("word",)

    def get_primary_translation(self, obj: Word) -> str:
        if isinstance(obj.full_translation, dict):
            return str(obj.full_translation.get("primary_translation", ""))
        return ""

    get_primary_translation.short_description = "Перевод"


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "status", "added_at")
    list_filter = ("status", "added_at")
    search_fields = ("user__email", "word__word")
