from django.contrib import admin
from apps.films.models import Film


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["title", "youtube_url", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["created_at"]
