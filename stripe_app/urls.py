from django.urls import path

from stripe_app import views

app_name = "stripe-app"
urlpatterns = [
    path(
        "organization/<str:org_id>/charge/",
        views.organization_onboarding_charge,
        name="organization-onboarding-charge",
    ),
    path("payment/secret/", views.client_secret, name="payment-intent-view"),
    path("payment/status/", views.payment_status, name="payment-status"),
]
