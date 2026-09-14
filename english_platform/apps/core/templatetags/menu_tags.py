from typing import Any

from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()

MENU_ITEMS: list[dict[str, str]] = [
    {"title": "Словарь", "url_name": "dictionary:search", "icon": "📖"},
    {"title": "Таблицы", "url_name": "", "icon": "📋"},
    {"title": "Книги", "url_name": "", "icon": "📚"},
    {"title": "Кино", "url_name": "", "icon": "🎬"},
    {"title": "Скролл", "url_name": "", "icon": "📱"},
    {"title": "Кабинет", "url_name": "", "icon": "👤"},
]


@register.simple_tag(takes_context=True)
def get_menu(context: dict[str, Any]) -> list[dict[str, Any]]:
    request = context.get("request")
    current_path: str = request.path if request else ""

    resolved: list[dict[str, Any]] = []
    for item in MENU_ITEMS:
        entry: dict[str, Any] = {
            "title": item["title"],
            "icon": item["icon"],
            "active": False,
            "disabled": True,
            "url": "#",
        }

        if item["url_name"]:
            try:
                url = reverse(item["url_name"])
                entry["url"] = url
                entry["disabled"] = False
                entry["active"] = current_path.startswith(url)
            except NoReverseMatch:
                pass

        resolved.append(entry)

    return resolved
