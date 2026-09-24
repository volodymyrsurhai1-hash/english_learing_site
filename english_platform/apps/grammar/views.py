from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, TemplateView

from apps.grammar.data import CATEGORIES
from apps.grammar.models import Topic
from apps.grammar.services import (
    TopicNotFoundError,
    create_ai_topic,
    delete_user_topic,
    get_accessible_topics_queryset,
    get_topics_queryset,
    get_user_topics_queryset,
)


class GrammarListView(TemplateView):
    template_name: str = "grammar/list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        q: str = self.request.GET.get("q", "").strip()
        category: str = self.request.GET.get("category", "").strip()
        level: str = self.request.GET.get("level", "").strip()

        topics = get_topics_queryset(q=q, category=category, level=level)

        grouped: dict[str, list[Topic]] = {}
        cat_labels: dict[str, str] = dict(CATEGORIES)

        for topic in topics:
            cat_label: str = cat_labels.get(topic.category) or str(topic.category)
            if cat_label not in grouped:
                grouped[cat_label] = []
            grouped[cat_label].append(topic)

        ctx["topics"] = topics
        ctx["grouped"] = grouped
        ctx["categories"] = CATEGORIES
        ctx["levels"] = ["A1", "A2", "B1", "B2"]
        ctx["selected_category"] = category
        ctx["selected_level"] = level
        ctx["query"] = q

        if self.request.user.is_authenticated:
            ctx["my_topics_count"] = Topic.objects.filter(
                user=self.request.user
            ).count()
        else:
            ctx["my_topics_count"] = 0

        return ctx


class MyGrammarListView(LoginRequiredMixin, TemplateView):
    template_name: str = "grammar/my_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        q: str = self.request.GET.get("q", "").strip()

        topics = get_user_topics_queryset(user=self.request.user, q=q)
        ctx["topics"] = topics
        ctx["query"] = q
        ctx["total_count"] = topics.count()
        return ctx


class DeleteTopicView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        delete_user_topic(slug=slug, user=request.user)
        return redirect("grammar:my_list")


class GrammarDetailView(DetailView):
    model = Topic
    template_name: str = "grammar/detail.html"
    context_object_name: str = "topic"
    slug_field: str = "slug"
    slug_url_kwarg: str = "slug"

    def get_queryset(self):
        return get_accessible_topics_queryset(self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        topic: Topic = self.get_object()
        cat_labels: dict[str, str] = dict(CATEGORIES)
        ctx["category_label"] = cat_labels.get(topic.category, topic.category)
        return ctx


class AddTopicView(LoginRequiredMixin, View):
    template_name: str = "grammar/add_topic.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        topic_name: str = request.POST.get("topic_name", "").strip()
        if not topic_name:
            return render(
                request,
                self.template_name,
                {"error": "Пожалуйста, введите название темы."},
            )

        try:
            topic: Topic = create_ai_topic(topic_name, request.user)
            return redirect(topic.get_absolute_url())
        except TopicNotFoundError as exc:
            return render(
                request,
                self.template_name,
                {"error": str(exc), "topic_name": topic_name},
            )
        except Exception as exc:
            return render(
                request,
                self.template_name,
                {
                    "error": f"Произошла ошибка при генерации темы: {exc}",
                    "topic_name": topic_name,
                },
            )
