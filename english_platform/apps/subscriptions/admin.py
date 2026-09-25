from typing import Any
from django.contrib import admin
from django.http import HttpRequest

from .models import Plan, UsageRecord


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "code",
        "name",
        "daily_video_limit",
        "daily_grammar_limit",
        "patreon_tier_id",
    ]
    list_filter: list[str] = ["code"]
    search_fields: list[str] = ["name", "code", "patreon_tier_id"]
    ordering: list[str] = ["code"]


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display: list[str] = ["user", "action_type", "created_at"]
    list_filter: list[str] = ["action_type", "created_at"]
    search_fields: list[str] = ["user__email"]
    ordering: list[str] = ["-created_at"]
    readonly_fields: list[str] = ["user", "action_type", "created_at"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = None
    ) -> bool:
        return False
