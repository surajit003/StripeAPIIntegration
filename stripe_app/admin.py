from django.contrib import admin

from stripe_app import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_id',)


@admin.register(models.PaymentIntent)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('intent_id', 'charge_amount', "organization",)
