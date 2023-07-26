import re
import requests
from datetime import date, timedelta

# django imports
from django.db import models
from django.conf import settings

# collaberr imports
from core.plugins.youtube_analytics.query import YoutubeQueryHook


class Creator(models.Model):
    class Meta:
        db_table = 'creators'
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'

    id = models.AutoField(primary_key=True)

    account_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='creator',
        db_column='account_id',
    )
    earnings = models.PositiveIntegerField(default=0)
    channel_id = models.CharField(max_length=100, null=True, blank=True)
    channel_name = models.CharField(max_length=100, null=True, blank=True)
    channel_handle = models.CharField(max_length=100, null=True, blank=True)
    channel_verified = models.BooleanField(default=False)
    channel_registered_date = models.DateField(null=True, blank=True)
    channel_report_generated = models.BooleanField(default=False)

    def request_campaign(self, campaign):
        if campaign not in self.requested_campaigns.all():
            self.requested_campaigns.add(campaign)
            self.save()
        else:
            raise Exception('Already requested')

    def get_channel_id_from_handle(self, channel_handle: str):
        if channel_handle.find('@') == -1:
            channel_handle = '@' + channel_handle
        url = 'https://www.youtube.com/' + channel_handle
        response = requests.get(url)

        if response.status_code == 200:
            channel_id = re.findall(
                '<meta itemprop="identifier" content="([^"]*)"',
                response.text
            )[0]
            channel_name = re.findall(
                '<meta itemprop="name" content="([^"]*)"',
                response.text
            )[0]
            return channel_id, channel_name
        else:
            return False

    # Could be a better way to verify channel but this works for now
    def verify_channel(self, **credentials):
        """
        Verify channel based on query result from
        credentials and channel_id
        """
        self.channel_id, self.channel_name = self.get_channel_id_from_handle(self.channel_handle)
        query_params = {
            'channel_id': self.channel_id,
            'start_date': date.today() - timedelta(days=5),
            'end_date': date.today() - timedelta(days=3),
            'metrics': 'views',
            'dimensions': 'day',
            'sort': '-views',
        }
        youtube_query_hook = YoutubeQueryHook(**credentials)
        query_result = youtube_query_hook.get_query(**query_params)
        if query_result:
            self.channel_verified = True
            self.channel_registered_date = date.today()
            # add celery task to update channel_report_generated field
            self.save()
            return True
        else:
            raise Exception('Channel could not be verified')
