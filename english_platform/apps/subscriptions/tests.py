import hashlib
import hmac
import json
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import ActionType, Plan, PlanTier, UsageRecord
from .services import QuotaService

User = get_user_model()


class QuotaServiceTests(TestCase):
    def setUp(self) -> None:
        self.free_plan = Plan.objects.get(code=PlanTier.FREE)
        self.middle_plan = Plan.objects.get(code=PlanTier.MIDDLE)
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            plan=self.free_plan,
        )

    def test_free_plan_limits(self) -> None:
        self.assertEqual(
            QuotaService.get_limit(self.user, ActionType.VIDEO_DOWNLOAD), 2
        )
        self.assertEqual(
            QuotaService.get_limit(self.user, ActionType.GRAMMAR_GENERATION), 2
        )

    def test_can_consume_and_consumption_enforcement(self) -> None:
        self.assertTrue(QuotaService.can_consume(self.user, ActionType.VIDEO_DOWNLOAD))
        self.assertEqual(
            QuotaService.get_remaining(self.user, ActionType.VIDEO_DOWNLOAD),
            (2, 2),
        )

        QuotaService.consume(self.user, ActionType.VIDEO_DOWNLOAD)
        self.assertTrue(QuotaService.can_consume(self.user, ActionType.VIDEO_DOWNLOAD))
        self.assertEqual(
            QuotaService.get_remaining(self.user, ActionType.VIDEO_DOWNLOAD),
            (1, 2),
        )

        QuotaService.consume(self.user, ActionType.VIDEO_DOWNLOAD)
        self.assertFalse(QuotaService.can_consume(self.user, ActionType.VIDEO_DOWNLOAD))
        self.assertEqual(
            QuotaService.get_remaining(self.user, ActionType.VIDEO_DOWNLOAD),
            (0, 2),
        )

    def test_upgrade_plan_increases_limits(self) -> None:
        QuotaService.consume(self.user, ActionType.VIDEO_DOWNLOAD)
        QuotaService.consume(self.user, ActionType.VIDEO_DOWNLOAD)
        self.assertFalse(QuotaService.can_consume(self.user, ActionType.VIDEO_DOWNLOAD))

        self.user.plan = self.middle_plan
        self.user.save(update_fields=["plan"])

        self.assertTrue(QuotaService.can_consume(self.user, ActionType.VIDEO_DOWNLOAD))
        self.assertEqual(
            QuotaService.get_remaining(self.user, ActionType.VIDEO_DOWNLOAD),
            (8, 10),
        )


class PatreonWebhookTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("subscriptions:patreon_webhook")
        self.secret = "test-patreon-secret"
        setattr(settings, "PATREON_WEBHOOK_SECRET", self.secret)

        self.free_plan = Plan.objects.get(code=PlanTier.FREE)
        self.middle_plan = Plan.objects.get(code=PlanTier.MIDDLE)
        self.middle_plan.patreon_tier_id = "tier_middle_123"
        self.middle_plan.save(update_fields=["patreon_tier_id"])

        self.user = User.objects.create_user(
            email="patron@example.com",
            password="testpassword123",
            plan=self.free_plan,
        )

    def _generate_signature(self, body: bytes) -> str:
        return hmac.new(
            self.secret.encode("utf-8"),
            body,
            hashlib.md5,
        ).hexdigest()

    def test_invalid_signature_returns_403(self) -> None:
        payload = json.dumps({"data": {}}).encode("utf-8")
        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
            HTTP_X_PATREON_SIGNATURE="invalid_signature",
        )
        self.assertEqual(response.status_code, 403)

    def test_valid_webhook_upgrades_user_subscription(self) -> None:
        payload_data: dict[str, Any] = {
            "data": {
                "attributes": {
                    "email": "patron@example.com",
                    "patron_status": "active_patron",
                },
                "relationships": {
                    "currently_entitled_tiers": {
                        "data": [{"id": "tier_middle_123", "type": "tier"}]
                    }
                },
            }
        }
        raw_body = json.dumps(payload_data).encode("utf-8")
        signature = self._generate_signature(raw_body)

        response = self.client.post(
            self.url,
            data=raw_body,
            content_type="application/json",
            HTTP_X_PATREON_SIGNATURE=signature,
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.plan, self.middle_plan)

    def test_webhook_cancellation_reverts_user_to_free(self) -> None:
        self.user.plan = self.middle_plan
        self.user.save(update_fields=["plan"])

        payload_data: dict[str, Any] = {
            "data": {
                "attributes": {
                    "email": "patron@example.com",
                    "patron_status": "former_patron",
                },
                "relationships": {"currently_entitled_tiers": {"data": []}},
            }
        }
        raw_body = json.dumps(payload_data).encode("utf-8")
        signature = self._generate_signature(raw_body)

        response = self.client.post(
            self.url,
            data=raw_body,
            content_type="application/json",
            HTTP_X_PATREON_SIGNATURE=signature,
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.plan, self.free_plan)
