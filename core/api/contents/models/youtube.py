from django.db import models


class Content(models.Model):
    class Meta:
        db_table = 'content'
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        'creators.Creator',
        on_delete=models.CASCADE,
        related_name='content',
        db_column='owner_id',
    )
    content_type = models.TextField()
    channel_id = models.TextField()
    channel_name = models.TextField()
    video_id = models.TextField()
    video_title = models.TextField()
    video_description = models.TextField()
    video_url = models.URLField(max_length=255)
    post_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
