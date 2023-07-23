from rest_framework import serializers
from core.api.youtube_analytics.models import YoutubeChannelBasic
from core.api.creators.models import Creator
from core.api.accounts.models import Account


class YoutubeChannelBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeChannelBasic
        fields = '__all__'

    # def validate(self, data):
    #     """
    #     Validate data, perform data type conversions, and handle related objects.
    #     """
    #     print(f'Validating data: {data}')
    #     subscribed_mapping = {'subscribed': True, 'not_subscribed': False}

    #     data['subscribed_status'] = subscribed_mapping.get(data['subscribed_status'], False)
    #     data['watch_time_minutes'] = float(data['watch_time_minutes'])
    #     data['average_view_duration_seconds'] = float(data['average_view_duration_seconds'])
    #     data['creator_id'] = Creator.objects.get(id=data['creator_id'])

    #     return data
