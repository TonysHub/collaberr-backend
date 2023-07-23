from django.db import models


class YoutubeReports(models.Model):
    """
    Display what kind of reports are available along with dates
    """
    class Meta:
        db_table = 'youtube_reports'
        verbose_name = 'Youtube Report'
        verbose_name_plural = 'Youtube Reports'

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    job_id = models.CharField(max_length=255)
    report_url = models.CharField(max_length=255)
    report_type = models.CharField(max_length=255)
    report_name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        'creators.Creator',
        on_delete=models.CASCADE,
        db_column='owner',
        related_name='youtube_reports',
    )

# yt_report_hook.create_reporting_job('channel_demographics_a1', 'Channel Demographics')

