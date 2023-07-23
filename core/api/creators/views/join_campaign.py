from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from core.api.campaigns.models import Campaign
from core.api.creators.models import Creator
from core.general.permissions import IsCreator

import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsCreator])
def request_to_join_campaign(request):
    campaign_id = request.data['campaign_id']
    campaign = Campaign.objects.get(id=campaign_id)
    if campaign.is_active and campaign.is_recruiting:
        creator = Creator.objects.get(account_id=request.user)
        campaign.add_requested_creator(creator)
        logger.info(f"Creator {creator} requested to join campaign {campaign}")
        return Response(status=status.HTTP_200_OK, data={'message': 'Successfully requested'})
    else:
        logger.info(f'Campaign {campaign} is not active')
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Campaign is not active'})
