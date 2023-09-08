# Generated by Django 4.2 on 2023-08-11 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_withdraw_transaction_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
