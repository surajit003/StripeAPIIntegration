# Generated by Django 4.0.4 on 2022-05-15 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0007_alter_payment_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Payment', 'verbose_name_plural': 'Payment'},
        ),
    ]