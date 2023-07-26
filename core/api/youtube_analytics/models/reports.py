from django.db import models


class YoutubeReportingJob(models.Model):
    """
    Display what kind of reports are requested to Youtube API
    This table is an aggregate of YoutubeReport table
    """
    class Meta:
        db_table = 'youtube_reporting_job'
        verbose_name = 'Youtube Reporting Job'
        verbose_name_plural = 'Youtube Reporting Jobs'

    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(
        'creators.Creator',
        on_delete=models.CASCADE,
        db_column='owner',
        related_name='youtube_reporting_job',
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    job_id = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)


# class YoutubeReport(models.Model):
#     """
#     Display reports in database
#     """
#     class Meta:
#         db_table = 'youtube_report'
#         verbose_name = 'Youtube Report'
#         verbose_name_plural = 'Youtube Reports'

#     id = models.AutoField(primary_key=True)
#     owner = models.ForeignKey(
#         'creators.Creator',
#         on_delete=models.CASCADE,
#         db_column='owner',
#         related_name='youtube_report',
#     )
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     job_id = models.CharField(max_length=255)
#     job_type = models.CharField(max_length=255)
#     job_name = models.CharField(max_length=255)
