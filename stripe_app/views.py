import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from stripe_app import payment


@csrf_exempt
@require_http_methods(["POST", ])
def client_secret(request):
    try:
        data = json.loads(request.body)
        amount = data.get("amount")
        currency = data.get("currency")
        intent = payment.create_payment_intent(amount, currency)
    except payment.PaymentIntentError as exc:
        return JsonResponse({"error": str(exc)})
    return JsonResponse({"secret_key": intent.client_secret})


@require_http_methods(['GET', ])
def checkout(request):
    return render(request, "stripe_app/checkout.html")


@require_http_methods(["GET", ])
def payment_status(request):
    return render(request, "stripe_app/payment_status.html")
