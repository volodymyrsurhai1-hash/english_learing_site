from django.db import migrations


def create_plans(apps, schema_editor):
    Plan = apps.get_model("subscriptions", "Plan")
    User = apps.get_model("users", "User")

    free_plan, _ = Plan.objects.get_or_create(
        code="FREE",
        defaults={
            "name": "Free",
            "daily_video_limit": 2,
            "daily_grammar_limit": 2,
        },
    )

    Plan.objects.get_or_create(
        code="MIDDLE",
        defaults={
            "name": "Middle",
            "daily_video_limit": 10,
            "daily_grammar_limit": 15,
        },
    )

    Plan.objects.get_or_create(
        code="MAXIMUM",
        defaults={
            "name": "Maximum",
            "daily_video_limit": 50,
            "daily_grammar_limit": 50,
        },
    )

    User.objects.filter(plan__isnull=True).update(plan=free_plan)


def delete_plans(apps, schema_editor):
    Plan = apps.get_model("subscriptions", "Plan")
    Plan.objects.filter(code__in=["FREE", "MIDDLE", "MAXIMUM"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0001_initial"),
        ("users", "0002_user_plan"),
    ]

    operations = [
        migrations.RunPython(create_plans, delete_plans),
    ]