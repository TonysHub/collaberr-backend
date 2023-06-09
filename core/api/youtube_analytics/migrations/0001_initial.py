# Generated by Django 4.2.3 on 2023-07-11 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("creators", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="YoutubeReports",
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
            ],
            options={
                "verbose_name": "Youtube Report",
                "verbose_name_plural": "Youtube Reports",
                "db_table": "youtube_reports",
            },
        ),
        migrations.CreateModel(
            name="YoutubeCredential",
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
                ("token", models.TextField()),
                ("refresh_token", models.TextField()),
                ("token_uri", models.TextField()),
                ("client_id", models.TextField()),
                ("client_secret", models.TextField()),
                ("scope", models.TextField()),
                (
                    "creator_id",
                    models.ForeignKey(
                        db_column="creator_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="youtube_credentials",
                        to="creators.creator",
                    ),
                ),
            ],
            options={
                "verbose_name": "Youtube Credential",
                "verbose_name_plural": "Youtube Credentials",
                "db_table": "youtube_credential",
            },
        ),
    ]
