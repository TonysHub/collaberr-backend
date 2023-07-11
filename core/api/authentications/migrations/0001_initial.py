# Generated by Django 4.2.3 on 2023-07-11 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JWTToken",
            fields=[
                (
                    "account_id",
                    models.OneToOneField(
                        db_column="account_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("refresh_token", models.TextField()),
                ("access_token", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("refresh_expires_at", models.DateTimeField()),
                ("access_expires_at", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "JWTToken",
                "verbose_name_plural": "JWTTokens",
                "db_table": "jwttokens",
            },
        ),
    ]
