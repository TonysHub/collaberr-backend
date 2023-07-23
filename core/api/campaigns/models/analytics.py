from django.db import models
from django.conf import settings


# class CampaignBasic(models.Model):
#     class Meta:
#         db_table = 'campaign_basics'
#         verbose_name = 'Campaign Basic'
#         verbose_name_plural = 'Campaign Basics'

#     campaign_id = models.OneToOneField(
#         'campaigns.Campaign',
#         on_delete=models.CASCADE,
#         related_name='campaign_basics',
#         db_column='campaign_id',
#         primary_key=True
#     )
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='campaign_basics',
#     )
#     business_id = models.OneToOneField(
#         'businesses.Business',
#         on_delete=models.CASCADE,
#         related_name='campaign_basics',
#         db_column='business_id',
#     )
#     date = models.DateField()
#     earnings = models.DecimalField(max_digits=10, decimal_places=2)
#     views = models.PositiveIntegerField(default=0)
#     creators = models.ManyToManyField(
#         'creators.Creator',
#     )
#     average_watch_time_minutes = models.DecimalField(max_digits=10, decimal_places=2)
#     average_view_percentage = models.DecimalField(max_digits=10, decimal_places=2)
#     creator_impressions = models.PositiveIntegerField(default=0)
#     creator_clicks = models.PositiveIntegerField(default=0)
#     likes = models.PositiveIntegerField(default=0)
#     dislikes = models.PositiveIntegerField(default=0)
#     comments = models.PositiveIntegerField(default=0)
#     shares = models.PositiveIntegerField(default=0)


