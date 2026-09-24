from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from apps.dictionary.services import (
    delete_word_for_user,
    get_or_generate_word,
    is_word_saved,
    save_word_for_user,
    toggle_word_status,
    validate_query,
    WordNotFoundError,
)
from apps.dictionary.models import Word


class SearchView(TemplateView):
    template_name: str = "dictionary/search.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        query: str = self.request.GET.get("q", "").strip()
        context["query"] = query
        context["error"] = None

        if query:
            validation_error: Optional[str] = validate_query(query)
            if validation_error:
                context["error"] = validation_error
            else:
                try:
                    context["result"] = get_or_generate_word(query)
                    if self.request.user.is_authenticated:
                        context["is_saved"] = is_word_saved(query, self.request.user)
                    else:
                        context["is_saved"] = False
                except WordNotFoundError as exc:
                    context["error"] = str(exc)

        return context


class SaveWordView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        word_text: str = request.POST.get("word", "").strip()
        if word_text:
            try:
                save_word_for_user(word_text, request.user)
            except Word.DoesNotExist:
                pass
        return redirect(f"/?q={word_text}")


class DeleteWordView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        word_text: str = request.POST.get("word", "").strip()
        next_url: str = request.POST.get("next", "/")
        if word_text:
            delete_word_for_user(word_text, request.user)
        return redirect(next_url)


class ToggleWordStatusView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        word_text: str = request.POST.get("word", "").strip()
        next_url: str = request.POST.get("next", "/")
        if word_text:
            toggle_word_status(word_text, request.user)
        return redirect(next_url)
