import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeError(Exception):
    pass


class PaymentIntentError(StripeError):
    pass


def create_payment_intent(amount: int, currency_iso: str):
    try:
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency_iso,
            automatic_payment_methods={"enabled": True}, )
    except stripe.error.InvalidRequestError as e:
        raise PaymentIntentError(e)
