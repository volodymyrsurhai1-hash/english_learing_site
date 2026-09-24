from typing import Any

from django import template
from django.urls import NoReverseMatch, reverse

from django import template
from django.utils.safestring import mark_safe

import markdown

register = template.Library()

MENU_ITEMS: list[dict[str, str]] = [
    {"title": "Словарь", "url_name": "dictionary:search", "icon": "📖"},
    {"title": "Грамматика", "url_name": "grammar:list", "icon": "📚"},
    {"title": "Карточки", "url_name": "cards:index", "icon": "🃏"},
    {"title": "Кино", "url_name": "films:list", "icon": "🎬"},
    {"title": "Профиль", "url_name": "profile", "icon": "👤"},
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


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
