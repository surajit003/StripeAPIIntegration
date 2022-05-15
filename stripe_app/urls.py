from django.urls import path

from stripe_app import views

urlpatterns = [
    path("charge/<str:org_id>/", views.organization_charge, name="payment-charge-organization"),
    path("secret/", views.client_secret, name="payment-intent-view"),
    path("checkout/", views.checkout, name="payment-checkout"),
    path("status/", views.payment_status, name="payment-status"),
]
