from typing import Any

from django.conf import settings
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, default="tenses", db_index=True)
    level = models.CharField(max_length=10, default="B1", db_index=True)
    order = models.PositiveIntegerField(default=0)
    data = models.JSONField(default=dict)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="custom_topics",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["order", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.level})"

    def get_absolute_url(self) -> str:
        return reverse("grammar:detail", kwargs={"slug": self.slug})

    @property
    def essence(self) -> str:
        return self.data.get("essence", "")

    @property
    def formulas(self) -> list[dict[str, Any]]:
        return self.data.get("formulas", [])

    @property
    def formula_note(self) -> str:
        return self.data.get("formula_note", "")

    @property
    def scenarios(self) -> list[dict[str, Any]]:
        return self.data.get("scenarios", [])

    @property
    def markers(self) -> list[str]:
        return self.data.get("markers", [])

    @property
    def exercises(self) -> list[dict[str, Any]]:
        return self.data.get("exercises", [])
