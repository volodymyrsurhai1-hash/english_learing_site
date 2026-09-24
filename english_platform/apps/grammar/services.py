from typing import Any, Optional

from django.db.models import QuerySet
from django.utils.text import slugify

from apps.grammar.generator import generate_and_export_topic
from apps.grammar.models import Topic


class TopicNotFoundError(Exception):
    pass


from django.db.models import Q, QuerySet


def get_topics_queryset(
    q: str = "", category: str = "", level: str = ""
) -> QuerySet[Topic]:
    queryset: QuerySet[Topic] = Topic.objects.filter(user__isnull=True)
    if category:
        queryset = queryset.filter(category=category)
    if level:
        queryset = queryset.filter(level=level)
    if q:
        queryset = queryset.filter(title__icontains=q)
    return queryset


def create_ai_topic(topic_name: str, user: Any) -> Topic:
    normalized: str = topic_name.strip()
    if not normalized:
        raise ValueError("Название темы не может быть пустым.")

    analysis: dict[str, Any] = generate_and_export_topic(normalized)

    if not analysis.get("is_valid", True):
        raise TopicNotFoundError(
            f"«{normalized}» не удалось распознать как тему английской грамматики."
        )

    base_slug: str = slugify(analysis.get("slug", "") or normalized)
    slug: str = base_slug
    counter: int = 1
    while Topic.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    topic: Topic = Topic.objects.create(
        slug=slug,
        title=analysis.get("title", normalized),
        subtitle=analysis.get("subtitle", ""),
        category=analysis.get("category", "tenses"),
        level=analysis.get("level", "B1"),
        data=analysis,
        user=user if getattr(user, "is_authenticated", False) else None,
    )
    return topic


def get_user_topics_queryset(user: Any, q: str = "") -> QuerySet[Topic]:
    queryset: QuerySet[Topic] = Topic.objects.filter(user=user)
    if q:
        queryset = queryset.filter(title__icontains=q)
    return queryset


def delete_user_topic(slug: str, user: Any) -> bool:
    deleted_count, _ = Topic.objects.filter(slug=slug, user=user).delete()
    return deleted_count > 0


def get_accessible_topics_queryset(user: Any) -> QuerySet[Topic]:
    if user and getattr(user, "is_authenticated", False):
        return Topic.objects.filter(Q(user__isnull=True) | Q(user=user))
    return Topic.objects.filter(user__isnull=True)
