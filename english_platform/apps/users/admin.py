from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "plan", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "plan"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Subscription", {"fields": ("plan",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "plan",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
