from django.db import models
from django.conf import settings


class YoutubeCredential(models.Model):
    class Meta:
        db_table = 'youtube_credentials'
        verbose_name = 'Youtube Credential'
        verbose_name_plural = 'Youtube Credentials'

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='account_id',
        primary_key=True,
    )
    creator_id = models.ForeignKey(
        'creators.Creator',
        on_delete=models.CASCADE,
        db_column='creator_id',
        related_name='youtube_credentials',
    )
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()
