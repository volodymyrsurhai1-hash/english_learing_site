import hashlib
import hmac
import json
import logging
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Plan, PlanTier

logger = logging.getLogger(__name__)

User = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class PatreonWebhookView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        secret: str = getattr(settings, "PATREON_WEBHOOK_SECRET", "")
        if not secret:
            logger.error("PATREON_WEBHOOK_SECRET is not configured")
            return HttpResponse(status=500)

        signature: str = request.headers.get("X-Patreon-Signature", "")
        digest: str = hmac.new(
            secret.encode("utf-8"),
            request.body,
            hashlib.md5,
        ).hexdigest()

        if not hmac.compare_digest(digest, signature):
            logger.warning("Patreon webhook signature mismatch: received %s", signature)
            return HttpResponse(status=403)

        try:
            payload: dict[str, Any] = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from Patreon webhook payload")
            return HttpResponse(status=400)

        data: dict[str, Any] = payload.get("data", {})
        attributes: dict[str, Any] = data.get("attributes", {})
        email: str = attributes.get("email", "")
        patron_status: str = attributes.get("patron_status", "")

        if not email:
            included: list[dict[str, Any]] = payload.get("included", [])
            for item in included:
                if item.get("type") == "user":
                    email = item.get("attributes", {}).get("email", "")
                    if email:
                        break

        if not email:
            return HttpResponse(status=200)

        user = User.objects.filter(email=email).first()
        if not user:
            return HttpResponse(status=200)

        free_plan: Plan | None = Plan.objects.filter(code=PlanTier.FREE).first()

        if patron_status == "active_patron":
            relationships: dict[str, Any] = data.get("relationships", {})
            tiers_data: list[dict[str, Any]] = relationships.get(
                "currently_entitled_tiers", {}
            ).get("data", [])
            tier_id: str | None = tiers_data[0].get("id") if tiers_data else None

            plan: Plan | None = (
                Plan.objects.filter(patreon_tier_id=tier_id).first()
                if tier_id
                else None
            )
            user.plan = plan or free_plan
        else:
            user.plan = free_plan

        user.save(update_fields=["plan"])
        logger.info(
            "Patreon webhook updated plan for user %s to %s (patron_status: %s)",
            user.email,
            user.plan.name if user.plan else "None",
            patron_status,
        )
        return HttpResponse(status=200)
