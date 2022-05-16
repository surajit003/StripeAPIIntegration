import json

from django.http import JsonResponse
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from stripe_app import payment
from stripe_app.models import Organization
from stripe_app.models import Payment


@csrf_exempt
@require_http_methods(
    [
        "POST",
    ]
)
def client_secret(request):
    try:
        data = json.loads(request.body)
        amount = data.get("amount")
        currency = data.get("currency")
        organization_id = data.get("organization_id")
        charge_type = data.get("charge_type")
        intent = payment.create_payment_intent(
            amount, currency, organization_id, charge_type
        )
    except payment.PaymentIntentError as exc:
        return JsonResponse({"error": str(exc)})
    return JsonResponse({"secret_key": intent.client_secret})


@require_http_methods(
    [
        "GET",
    ]
)
def organization_onboarding_charge(request, org_id):
    organization = Organization.objects.filter(org_id=org_id).first()
    if organization:
        _payment = Payment.objects.filter(
            organization=organization, charge_type="ONBOARDING"
        ).first()
        if not _payment.paid:
            amount = _payment.charge_amount
            return render(
                request,
                "stripe_app/checkout.html",
                {
                    "amount": amount,
                    "organization_id": org_id,
                    "charge_type": "ONBOARDING",
                },
            )
        else:
            return HttpResponse(
                "Onboarding payment has already been made for this organization"
            )
    else:
        raise Http404("Invalid Organization")


@require_http_methods(
    [
        "GET",
    ]
)
def payment_status(request):
    payment_intent_id = request.GET.get("payment_intent")
    payment_intent = payment.get_payment_intent(payment_intent_id)
    organization_id = payment_intent["metadata"]["organization_id"]
    charge_type = payment_intent["metadata"]["charge_type"]
    _payment_status = payment_intent["charges"]["data"][0]["paid"]
    Payment.objects.filter(
        organization__org_id=organization_id, charge_type=charge_type
    ).update(
        transaction_id=payment_intent_id, paid=_payment_status, response=payment_intent
    )
    return render(request, "stripe_app/payment_status.html")
