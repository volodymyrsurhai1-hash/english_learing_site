from django.conf import settings
from django.db import models


class PlanTier(models.TextChoices):
    FREE = "FREE", "Free"
    MIDDLE = "MIDDLE", "Middle"
    MAXIMUM = "MAXIMUM", "Maximum"


class ActionType(models.TextChoices):
    VIDEO_DOWNLOAD = "VIDEO_DOWNLOAD", "Скачивание видео"
    GRAMMAR_GENERATION = "GRAMMAR_GENERATION", "Генерация грамматики"


class Plan(models.Model):
    code = models.CharField(
        max_length=20,
        choices=PlanTier.choices,
        unique=True,
    )
    name = models.CharField(max_length=50)
    daily_video_limit = models.PositiveIntegerField(default=2)
    daily_grammar_limit = models.PositiveIntegerField(default=2)
    patreon_tier_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class UsageRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usage_records",
    )
    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "action_type", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.action_type} ({self.created_at})"