import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from core.api.creators.models import Creator
from core.api.youtube_analytics.models import YoutubeChannelBasic
from core.api.youtube_analytics.serializers import YoutubeChannelBasicSerializer

logger = logging.getLogger(__name__)


class CreatorStatsView(APIView):
    """
    Get creator stats from Youtube API
    3 day delay
    """
    queryset = YoutubeChannelBasic.objects.all()
    serializer_class = YoutubeChannelBasicSerializer
    premission_classes = [AllowAny]

    def post(self, request):
        creator_id = request.data['creator_id']
        if not Creator.objects.get(id=creator_id).channel_report_generated:
            logger.info(f'Report not generated for creator {creator_id}')
            return Response({'message': 'Report not generated'}, status=400)

        response = self.queryset.filter(creator_id=creator_id)
        serializer = self.serializer_class(response, many=True)
        return Response(serializer.data, status=200)

    def get_permissions(self):
        return [AllowAny()]

    # if generated date + 3 <= today:
    # have to wait 3 days to generate new stats
    # if data is not present in db:
    # perform bulk create
    # if data is present:
    # show data
