from rest_framework import serializers
from core.api.youtube_analytics.models import YoutubeReportingJob


class YoutubeReportingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeReportingJob
        fields = ['job_id', 'job_type', 'job_name']
