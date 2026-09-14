from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.dictionary.services import get_or_generate_word


class SearchView(LoginRequiredMixin, TemplateView):
    template_name: str = "dictionary/search.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        query: str = self.request.GET.get("q", "").strip()
        context["query"] = query

        if query:
            context["result"] = get_or_generate_word(query)

        return context
