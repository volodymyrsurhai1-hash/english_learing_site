from typing import Callable

from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

_OTP_EXEMPT_PREFIXES: tuple[str, ...] = (
    "/account/login/",
    "/accounts/register/",
    "/accounts/logout/",
    "/admin/",
    "/static/",
    "/media/",
)


class EnforceOTPMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated and not request.user.is_verified():
            if request.path.startswith("/account/login/"):
                logout(request)
            elif not any(
                request.path.startswith(prefix) for prefix in _OTP_EXEMPT_PREFIXES
            ):
                next_path = request.path
                logout(request)
                login_url = reverse("two_factor:login")
                return redirect(f"{login_url}?next={next_path}")

        return self.get_response(request)
