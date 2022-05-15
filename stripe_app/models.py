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


class PaymentIntent(TimeStampedModel):
    intent_id = models.CharField(max_length=255)
    charge_amount = models.IntegerField(default=11900)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'PaymentIntent id {self.intent_id} for Organization Name {self.organization.name} '

    class Meta:
        verbose_name = _("PaymentIntent")
        verbose_name_plural = _("PaymentIntent")
