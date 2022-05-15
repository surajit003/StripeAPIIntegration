from django.contrib import admin

from stripe_app import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_id',)


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'charge_amount', "organization", "paid",)
    readonly_fields = ("paid",)
