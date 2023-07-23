from django.db import models
from django.conf import settings


class YoutubeChannelBasic(models.Model):
    """
    Based on channel_basic_a2
    Only verified channel will have this report
    Aggregated on date, video_id, subscribed_status, country_code
    """
    class Meta:
        db_table = 'youtube_channel_basics'
        verbose_name = 'Youtube Channel Basic'
        verbose_name_plural = 'Youtube Channel Basics'

    creator_id = models.ForeignKey(
        'creators.Creator',
        on_delete=models.CASCADE,
        related_name='creator_basics',
        db_column='creator_id',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='creator_basics',
    )
    # dimensions
    date = models.DateField()
    channel_id = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=100)
    channel_handle = models.CharField(max_length=100)
    video_id = models.CharField(max_length=100, blank=True, null=True)
    subscribed_status = models.BooleanField(default=False)
    country_code = models.CharField(max_length=4)
    # core metrics
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    watch_time_minutes = models.FloatField(default=0)
    average_view_duration_seconds = models.FloatField(default=0)
    average_view_duration_percentage = models.FloatField(default=0)
    subscribers_gained = models.IntegerField(default=0)
    subscribers_lost = models.IntegerField(default=0)
    # additional metrics
    annotation_impressions = models.IntegerField(default=0)
    annotation_clicks = models.IntegerField(default=0)
    annotation_click_through_rate = models.IntegerField(default=0)
    card_impressions = models.IntegerField(default=0)
    card_clicks = models.IntegerField(default=0)
    card_click_through_rate = models.IntegerField(default=0)
    videos_added_to_playlists = models.IntegerField(default=0)
    videos_removed_from_playlists = models.IntegerField(default=0)
    red_views = models.IntegerField(default=0)
    red_watch_time_minutes = models.FloatField(default=0)

# class ChannelDemographics(models.Model):
#     """
#     Based on channel_traffic_source_a2
#     Only verified channel will have this report
#     Aggregated on date, video_id, subscribed_status, country_code
#     """
