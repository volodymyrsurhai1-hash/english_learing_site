from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.dictionary.models import UserWord


class FlashcardRedirectView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        first: Optional[UserWord] = (
            UserWord.objects.filter(user=request.user, status="LEARNING")
            .select_related("word")
            .order_by("added_at")
            .first()
        )
        if first is None:
            return render(request, "cards/done.html")
        return redirect("cards:card", pk=first.pk)


class FlashcardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        learning_qs = (
            UserWord.objects.filter(user=request.user, status="LEARNING")
            .select_related("word")
            .order_by("added_at")
        )

        if not learning_qs.exists():
            return render(request, "cards/done.html")

        current: UserWord = get_object_or_404(UserWord, pk=pk, user=request.user)

        pks: list[int] = list(learning_qs.values_list("pk", flat=True))
        total: int = len(pks)

        try:
            current_index: int = pks.index(current.pk)
        except ValueError:
            return redirect("cards:index")

        next_pk: Optional[int] = (
            pks[current_index + 1] if current_index + 1 < total else None
        )
        progress: int = current_index + 1

        all_qs = UserWord.objects.filter(user=request.user)
        total_all: int = all_qs.count()
        count_learned: int = all_qs.filter(status="LEARNED").count()

        context: dict[str, Any] = {
            "user_word": current,
            "next_pk": next_pk,
            "count_learned": count_learned,
            "total_all": total_all,
            "remaining": total,
        }
        return render(request, "cards/card.html", context)


class MarkLearnedView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        user_word: UserWord = get_object_or_404(UserWord, pk=pk, user=request.user)
        user_word.status = "LEARNED"
        user_word.save(update_fields=["status"])

        next_pk_str: str = request.POST.get("next_pk", "")
        if next_pk_str.isdigit():
            return redirect("cards:card", pk=int(next_pk_str))
        return redirect("cards:index")
