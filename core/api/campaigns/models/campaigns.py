from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxLengthValidator

# from core.api.campaigns.managers import CampaignManager
from core.general.models import CreatedModified

import logging
logger = logging.getLogger(__name__)


class Campaign(CreatedModified):
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        db_table = 'campaigns'

    class Category(models.TextChoices):
        FASHION = 'Fashion'
        BEAUTY = 'Beauty'
        FOOD = 'Food'
        TRAVEL = 'Travel'
        BEVERAGES = 'Beverages'

    class Platform(models.TextChoices):
        INSTAGRAM = 'Instagram'
        YOUTUBE = 'Youtube'
        TIKTOK = 'Tiktok'

    class MissionType(models.TextChoices):
        YOUTUBE_VIDEO = 'Youtube Video'
        YOUTUBE_SHORTS = 'Youtube Shorts'
        POST = 'Post'
        STORY = 'Story'
        REEL = 'Reel'
        IGTV = 'IGTV'
        TIKTOK_VIDEO = 'Tiktok Video'

    # objects = CampaignManager()

    id = models.AutoField(
            primary_key=True,
            unique=True,
            editable=False
        )
    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE
        )
    # fields that business owners fill
    brand_name = models.TextField(validators=[MaxLengthValidator(100)])
    title = models.TextField(validators=[MaxLengthValidator(100)])
    thumbnail = models.ImageField(
                            upload_to='campaigns/thumbnails/',
                            null=True,
                            blank=True
                        )
    thumbnail_url = models.URLField(null=True, blank=True)
    category = models.TextField(choices=Category.choices)
    platform = models.TextField(choices=Platform.choices)
    recruit_start_date = models.DateField()
    recruit_end_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    mission_type = models.TextField(choices=MissionType.choices)
    reward = models.PositiveIntegerField()
    additional_files = models.FileField(
                            upload_to='campaigns/additional_files/',
                            null=True,
                            blank=True
                        )
    # auto populated fields
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_recruiting = models.BooleanField(default=True)
    is_recruited = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # creator actions
    requested_creators = models.ManyToManyField(
                                'creators.Creator',
                                related_name='campaigns_requested',
                                blank=True
                            )
    approved_creators = models.ManyToManyField(
                                'creators.Creator',
                                related_name='campaigns_approved',
                                blank=True
                            )
    declined_creators = models.ManyToManyField(
                                'creators.Creator',
                                related_name='campaigns_declined',
                                blank=True
                            )

    # content actions
    content_submitted = models.ManyToManyField(
                                'contents.Content',
                                related_name='campaigns_submitted',
                                blank=True
                            )
    content_approved = models.ManyToManyField(
                                'contents.Content',
                                related_name='campaigns_approved',
                                blank=True
                            )
    content_declined = models.ManyToManyField(
                                'contents.Content',
                                related_name='campaigns_declined',
                                blank=True
                            )

    def add_requested_creator(self, creator):
        if creator in self.requested_creators.all():
            logger.info(f'{creator} already requested to join {self}')
            raise Exception(f'{creator} already requested to join {self}')
        self.requested_creators.add(creator)
        logger.info(f'{creator} requested to join {self}')
        self.save()

    def add_approved_creator(self, creator):
        self.requested_creators.remove(creator)
        self.approved_creators.add(creator)
        if creator in self.declined_creators.all():
            self.declined_creators.remove(creator)
        logger.info(f'{creator} approved to join {self}')
        self.save()

    def add_declined_creator(self, creator):
        self.requested_creators.remove(creator)
        self.declined_creators.add(creator)
        if creator in self.approved_creators.all():
            self.approved_creators.remove(creator)
        logger.info(f'{creator} declined to join {self}')
        self.save()

    def add_content_submitted(self, content):
        self.content_submitted.add(content)
        logger.info(f'{content} submitted to {self}')
        self.save()

    def add_content_approved(self, content):
        self.content_submitted.remove(content)
        self.content_approved.add(content)
        if content in self.content_declined.all():
            self.content_declined.remove(content)
        logger.info(f'{content} approved to {self}')
        self.save()

    def add_content_declined(self, content):
        self.content_submitted.remove(content)
        self.content_declined.add(content)
        if content in self.content_approved.all():
            self.content_approved.remove(content)
        logger.info(f'{content} declined to {self}')
        self.save()

    def __str__(self):
        return f'{self.title} | {self.brand_name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)
