import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeError(Exception):
    pass


class PaymentIntentError(StripeError):
    pass


def create_payment_intent(
    amount: int, currency_iso: str, organization_id: str, charge_type: str
):
    try:
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency_iso,
            automatic_payment_methods={"enabled": True},
            metadata={"organization_id": organization_id, "charge_type": charge_type},
        )
    except stripe.error.InvalidRequestError as e:
        raise PaymentIntentError(e)


def get_payment_intent(payment_intent_id):
    payment_intent = stripe.PaymentIntent.retrieve(
        payment_intent_id,
    )
    return payment_intent
