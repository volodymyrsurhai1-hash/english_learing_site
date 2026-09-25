from datetime import timedelta
from typing import Any

from django.utils import timezone

from apps.subscriptions.models import ActionType, Plan, UsageRecord


class QuotaService:
    @staticmethod
    def get_limit(user: Any, action_type: str) -> int:
        plan: Plan | None = getattr(user, "plan", None)
        if not plan:
            return 2

        if action_type == ActionType.VIDEO_DOWNLOAD:
            return plan.daily_video_limit
        if action_type == ActionType.GRAMMAR_GENERATION:
            return plan.daily_grammar_limit

        return 0

    @classmethod
    def can_consume(cls, user: Any, action_type: str) -> bool:
        if not user or not user.is_authenticated:
            return False

        limit: int = cls.get_limit(user, action_type)
        since = timezone.now() - timedelta(hours=24)

        current_usage: int = UsageRecord.objects.filter(
            user=user,
            action_type=action_type,
            created_at__gte=since,
        ).count()

        return current_usage < limit

    @staticmethod
    def consume(user: Any, action_type: str) -> None:
        UsageRecord.objects.create(
            user=user,
            action_type=action_type,
        )

    @classmethod
    def get_remaining(cls, user: Any, action_type: str) -> tuple[int, int]:
        if not user or not user.is_authenticated:
            return 0, 0

        limit: int = cls.get_limit(user, action_type)
        since = timezone.now() - timedelta(hours=24)

        current_usage: int = UsageRecord.objects.filter(
            user=user,
            action_type=action_type,
            created_at__gte=since,
        ).count()

        remaining: int = max(0, limit - current_usage)
        return remaining, limit
