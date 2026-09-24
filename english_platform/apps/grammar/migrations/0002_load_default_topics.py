from dataclasses import asdict
from typing import Any

from django.db import migrations


def load_default_topics(apps: Any, schema_editor: Any) -> None:
    Topic = apps.get_model("grammar", "Topic")
    from apps.grammar.data import TOPICS

    for t in TOPICS:
        Topic.objects.update_or_create(
            slug=t.slug,
            defaults={
                "title": t.title,
                "subtitle": t.subtitle,
                "category": t.category,
                "level": t.level,
                "order": t.order,
                "data": {
                    "essence": t.essence,
                    "formulas": [asdict(f) for f in t.formulas],
                    "formula_note": t.formula_note,
                    "scenarios": [asdict(s) for s in t.scenarios],
                    "markers": t.markers,
                    "exercises": [asdict(e) for e in t.exercises],
                },
                "user": None,
            },
        )


def unload_default_topics(apps: Any, schema_editor: Any) -> None:
    Topic = apps.get_model("grammar", "Topic")
    Topic.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("grammar", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_default_topics, reverse_code=unload_default_topics),
    ]
