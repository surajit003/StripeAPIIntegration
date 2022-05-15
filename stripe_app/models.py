from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, editable=False, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    org_id = models.CharField(max_length=120, unique=True, db_index=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'Organization Id#{self.org_id} for organization {self.name}'


class Payment(TimeStampedModel):
    CHARGE_TYPE = (
        ("ONBOARDING", "Onboarding"),
        ("MAINTENANCE COST", "Charge for Maintenance"),
    )
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    charge_amount = models.IntegerField()
    charge_type = models.CharField(max_length=100, choices=CHARGE_TYPE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'PaymentIntent id {self.transaction_id} for Organization Name {self.organization.name} '

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payment")
        unique_together = ('charge_type', "organization")
