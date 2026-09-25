from typing import Any

from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpRequest


@receiver(user_logged_in)
def notify_user_login(
    sender: Any, request: HttpRequest, user: Any, **kwargs: Any
) -> None:
    if request:
        messages.success(request, f"С возвращением! Вы успешно вошли в аккаунт.")
