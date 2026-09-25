from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(
        "subscriptions.Plan",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        []
    )  # поля, которые спросит createsuperuser кроме USERNAME_FIELD и пароля

    def __str__(self):
        return self.email
