import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount: int, currency_iso: str):
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=currency_iso,
        automatic_payment_methods={"enabled": True},
    )
