# Generated by Django 4.0.4 on 2022-05-15 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stripe_app", "0006_payment_charge_type"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="payment",
            unique_together={("charge_type", "organization")},
        ),
    ]
