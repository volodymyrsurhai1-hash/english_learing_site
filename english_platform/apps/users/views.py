from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.users.forms import RegisterForm


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dictionary:search")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})