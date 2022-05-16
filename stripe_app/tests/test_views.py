import json
from unittest.mock import patch

from django.test import TestCase

from stripe_app.payment import PaymentIntentError
from stripe_app.models import Organization
from stripe_app.models import Payment


class MockStripePaymentIntent:
    def __init__(self, client_secret: str):
        self.client_secret = client_secret


class TestViews(TestCase):

    def setUp(self):
        organization = Organization.objects.create(org_id="PAM-123", name="Pass the Org")
        Payment.objects.create(organization=organization, charge_amount=100,
                               charge_type="ONBOARDING")

    @patch("stripe_app.views.payment.create_payment_intent")
    def test_client_secret_view(self, mock_create_payment_intent):
        data = {"amount": 34,
                "currency": "USD",
                "organization_id": 123,
                "charge_type": "ONBOARDING",
                }
        mock_stripe_payment_intent = MockStripePaymentIntent("Test-secret-key")
        mock_create_payment_intent.return_value = mock_stripe_payment_intent
        response = self.client.post('/stripe/payment/secret/', data=data,
                                    content_type="application/json")
        content = json.loads(response.content.decode("utf-8"))
        secret_key = content["secret_key"]
        self.assertEquals(response.status_code, 200)
        self.assertEquals(secret_key, "Test-secret-key")

    @patch("stripe_app.views.payment.create_payment_intent")
    def test_client_secret_view_raises_payment_intent_error(self, mock_create_payment_intent):
        data = {"amount": 34,
                "currency": "KES",
                "organization_id": 12,
                "charge_type": "ONBOARDING",
                }
        mock_create_payment_intent.side_effect = PaymentIntentError("Payment method not allowed")
        response = self.client.post('/stripe/payment/secret/', data=data,
                                    content_type="application/json")
        content = json.loads(response.content.decode("utf-8"))
        error = content["error"]
        self.assertEquals(response.status_code, 200)
        self.assertEquals(error, "Payment method not allowed")

    def test_organization_onboarding_charge(self):
        response = self.client.get('/stripe/organization/PAM-123/charge/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("stripe_app/checkout.html")

    def test_organization_onboarding_charge_for_duplicate_charge(self):
        Payment.objects.filter(organization__org_id="PAM-123", charge_type="ONBOARDING") \
            .update(paid=True)
        response = self.client.get('/stripe/organization/PAM-123/charge/')
        self.assertEquals(response.content.decode("utf-8"),
                          "Onboarding payment has already been made for this organization")

    def test_organization_onboarding_charge_for_invalid_organization(self):
        response = self.client.get('/stripe/organization/PAM-23/charge/')
        self.assertEquals(response.status_code, 404)

    @patch("stripe_app.payment.get_payment_intent")
    def test_payment_status(self, mock_get_payment_intent):
        stripe_payment_intent_resp = {
            "id": "1239-SJDKD",
            "metadata": {
                "organization_id": "PAM-123",
                "charge_type": "ONBOARDING"
            },
            "charges": {
                "data": [
                    {
                        "paid": True,
                    }
                ]
            }
        }

        mock_get_payment_intent.return_value = stripe_payment_intent_resp
        response = self.client.get('/stripe/payment/status/?payment_intent=1239-SJDKD')
        payment = Payment.objects.filter(organization__org_id="PAM-123",
                                         charge_type="ONBOARDING").first()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(payment.paid, True)
        self.assertEquals(payment.transaction_id, "1239-SJDKD")
        self.assertEquals(payment.response, stripe_payment_intent_resp)
