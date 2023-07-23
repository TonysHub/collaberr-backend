from django.http import HttpResponseBadRequest
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from core.general.permissions import IsBusiness
from core.api.creators.models import Creator
from core.api.creators.serializers import CreatorModelSerializer
from core.api.campaigns.models import Campaign

import logging
logger = logging.getLogger(__name__)


class CampaignCreatorsListView(ListAPIView):
    """
    List all creators.
    """
    queryset = Creator.objects.all()
    permission_classes = [IsBusiness]
    serializer_class = CreatorModelSerializer

    def get(self, request, campaign_id):
        try:
            Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return HttpResponseBadRequest('Campaign does not exist')

        requested_creators = self.get_queryset().filter(campaigns_requested__id=campaign_id)
        approved_creators = self.get_queryset().filter(campaigns_approved__id=campaign_id)
        declined_creators = self.get_queryset().filter(campaigns_declined__id=campaign_id)

        requested_creators = self.get_serializer(requested_creators, many=True).data
        approved_creators = self.get_serializer(approved_creators, many=True).data
        declined_creators = self.get_serializer(declined_creators, many=True).data

        response = {
            'requested': requested_creators,
            'approved': approved_creators,
            'declined': declined_creators
        }

        return Response(response)
