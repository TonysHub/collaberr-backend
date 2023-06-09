# Generated by Django 4.2.3 on 2023-07-11 07:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("creators", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.AutoField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "brand_name",
                    models.TextField(
                        validators=[django.core.validators.MaxLengthValidator(100)]
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        validators=[django.core.validators.MaxLengthValidator(100)]
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="campaigns/thumbnails/"
                    ),
                ),
                (
                    "category",
                    models.TextField(
                        choices=[
                            ("Fashion", "Fashion"),
                            ("Beauty", "Beauty"),
                            ("Food", "Food"),
                            ("Travel", "Travel"),
                            ("Beverages", "Beverages"),
                        ]
                    ),
                ),
                (
                    "platform",
                    models.TextField(
                        choices=[
                            ("Instagram", "Instagram"),
                            ("Youtube", "Youtube"),
                            ("Tiktok", "Tiktok"),
                        ]
                    ),
                ),
                ("recruit_start_date", models.DateField()),
                ("recruit_end_date", models.DateField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.TextField()),
                (
                    "mission_type",
                    models.TextField(
                        choices=[
                            ("Youtube Video", "Youtube Video"),
                            ("Youtube Shorts", "Youtube Shorts"),
                            ("Post", "Post"),
                            ("Story", "Story"),
                            ("Reel", "Reel"),
                            ("IGTV", "Igtv"),
                            ("Tiktok Video", "Tiktok Video"),
                        ]
                    ),
                ),
                ("reward", models.PositiveIntegerField()),
                (
                    "additional_files",
                    models.FileField(
                        blank=True, null=True, upload_to="campaigns/additional_files/"
                    ),
                ),
                ("created_at", models.DateTimeField(editable=False)),
                ("modified_at", models.DateTimeField()),
                ("is_draft", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_recruiting", models.BooleanField(default=True)),
                ("is_recruited", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "approved_creators",
                    models.ManyToManyField(
                        blank=True,
                        related_name="campaigns_approved",
                        to="creators.creator",
                    ),
                ),
                (
                    "declined_creators",
                    models.ManyToManyField(
                        blank=True,
                        related_name="campaigns_declined",
                        to="creators.creator",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requested_creators",
                    models.ManyToManyField(
                        blank=True,
                        related_name="campaigns_requested",
                        to="creators.creator",
                    ),
                ),
            ],
            options={
                "verbose_name": "Campaign",
                "verbose_name_plural": "Campaigns",
                "db_table": "campaigns",
            },
        ),
    ]
