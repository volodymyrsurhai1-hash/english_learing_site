from typing import Any

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django_otp.plugins.otp_email.models import EmailDevice

from apps.dictionary.models import UserWord
from apps.users.forms import RegisterForm


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            from apps.subscriptions.models import Plan

            user.plan = Plan.objects.filter(code="FREE").first()
            user.save()
            EmailDevice.objects.create(
                user=user,
                name="default",
                email=user.email,
                confirmed=True,
            )
            return redirect("two_factor:login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name: str = "accounts/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)

        status_filter: str = self.request.GET.get("status", "")
        valid_statuses: tuple[str, ...] = ("LEARNING", "LEARNED")

        queryset = (
            UserWord.objects.filter(user=self.request.user)
            .select_related("word")
            .order_by("-added_at")
        )

        if status_filter in valid_statuses:
            queryset = queryset.filter(status=status_filter)

        all_words = UserWord.objects.filter(user=self.request.user)
        context["words"] = queryset
        context["status_filter"] = status_filter
        context["count_all"] = all_words.count()
        context["count_learning"] = all_words.filter(status="LEARNING").count()
        context["count_learned"] = all_words.filter(status="LEARNED").count()

        return context
