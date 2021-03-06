# Generated by Django 4.0.4 on 2022-05-15 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PaymentIntent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("uid", models.CharField(max_length=255)),
                ("amount", models.IntegerField(default=11900)),
                (
                    "payment_organization",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("paid", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "PaymentIntent",
                "verbose_name_plural": "PaymentIntent",
            },
        ),
    ]
