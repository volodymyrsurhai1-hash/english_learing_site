from django.urls import path

from .views import PatreonWebhookView

app_name: str = "subscriptions"

urlpatterns = [
    path("patreon/webhook/", PatreonWebhookView.as_view(), name="patreon_webhook"),
]
