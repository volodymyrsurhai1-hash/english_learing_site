from datetime import date
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from apps.cards.services import DeckService
from apps.dictionary.models import UserWord
from apps.dictionary.presenters import CuratedDictionaryEntry, DictionaryPresenter


class FlashcardRedirectView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        deck = DeckService.get_or_create_deck(request.user)
        today: date = timezone.now().date()
        learned_today: int = UserWord.objects.filter(
            user=request.user, status="LEARNED", learned_at__date=today
        ).count()
        if not deck or learned_today >= settings.DAILY_WORD_GOAL:
            return render(request, "cards/done.html")

        return redirect("cards:card", pk=deck[0])


class FlashcardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        deck = DeckService.get_or_create_deck(request.user)
        if not deck:
            return render(request, "cards/done.html")

        current: UserWord = get_object_or_404(UserWord, pk=pk, user=request.user)

        next_pk: Optional[int] = DeckService.get_next_pk(request.user, current.pk)

        all_qs = UserWord.objects.filter(user=request.user)
        total_all: int = all_qs.count()
        today: date = timezone.now().date()
        count_learned: int = all_qs.filter(status="LEARNED").count()
        count_learned_today: int = all_qs.filter(
            status="LEARNED", learned_at__date=today
        ).count()

        entry: CuratedDictionaryEntry = DictionaryPresenter.present(
            current.word.full_translation, current.word.word
        )

        context: dict[str, Any] = {
            "user_word": current,
            "entry": entry,
            "next_pk": next_pk,
            "count_learned": count_learned,
            "total_all": total_all,
            "remaining": len(deck),
            "count_learned_today": count_learned_today,
            "daily_goal": settings.DAILY_WORD_GOAL,
        }
        return render(request, "cards/card.html", context)


class MarkLearnedView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        user_word: UserWord = get_object_or_404(UserWord, pk=pk, user=request.user)
        user_word.status = "LEARNED"
        user_word.learned_at = timezone.now()
        user_word.save(update_fields=["status", "learned_at"])
        DeckService.remove_pk(request.user, pk)

        today: date = timezone.now().date()
        learned_today: int = UserWord.objects.filter(
            user=request.user, status="LEARNED", learned_at__date=today
        ).count()
        if learned_today >= settings.DAILY_WORD_GOAL:
            return redirect("cards:index")

        next_pk_str: str = request.POST.get("next_pk", "")

        if next_pk_str.isdigit():
            return redirect("cards:card", pk=int(next_pk_str))
        return redirect("cards:index")
