from typing import Any

from django.http import HttpRequest

from apps.subscriptions.models import ActionType
from apps.subscriptions.services import QuotaService


def subscription_context(request: HttpRequest) -> dict[str, Any]:
    if not hasattr(request, "user") or not request.user.is_authenticated:
        return {}

    user = request.user
    video_remaining, video_limit = QuotaService.get_remaining(
        user, ActionType.VIDEO_DOWNLOAD
    )
    grammar_remaining, grammar_limit = QuotaService.get_remaining(
        user, ActionType.GRAMMAR_GENERATION
    )

    plan = getattr(user, "plan", None)

    return {
        "current_plan": plan,
        "video_quota": {
            "remaining": video_remaining,
            "limit": video_limit,
            "used": max(0, video_limit - video_remaining),
        },
        "grammar_quota": {
            "remaining": grammar_remaining,
            "limit": grammar_limit,
            "used": max(0, grammar_limit - grammar_remaining),
        },
        "patreon_url": "https://www.patreon.com/VSeng",
    }
