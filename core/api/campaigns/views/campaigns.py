from django_filters.rest_framework import DjangoFilterBackend

# DRF imports
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

# collaberr imports
from core.api.campaigns.models import Campaign
from core.api.campaigns.filters import CampaignFilter
from core.api.campaigns.serializers import CampaignCreateSerializer, CampaignReadSerializer
from core.general.permissions import IsObjectOwnerOrReadOnly, IsBusiness
from core.general.authentication import CustomJWTAuthentication


class CampaignViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampaignFilter
    # parser_classes = [FormParser, MultiPartParser, JSONParser]
    permission_classes = [IsObjectOwnerOrReadOnly, IsAuthenticated, IsBusiness]
    serializer_class = CampaignCreateSerializer
    authentication_classes = [CustomJWTAuthentication]
    queryset = Campaign.objects.filter(is_active=True).order_by('-created_at').all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        campaign = serializer.create(serializer.validated_data)
        read_serializer = CampaignReadSerializer(campaign)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj,
                                         data=request.data,
                                         partial=True,
                                         context={'request': request}
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Campaign.objects.select_related('owner').order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return CampaignCreateSerializer
        return CampaignReadSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated and IsBusiness()]
        elif self.action in ['retrieve', 'update', 'delete', 'partial_update']:
            return [IsObjectOwnerOrReadOnly()]
        elif self.action == 'get':
            return [AllowAny()]
        return super().get_permissions()


class CampaignReadOnlyViewSet(ReadOnlyModelViewSet):
    # paginate the queryset
    queryset = Campaign.objects.all()
    serializer_class = CampaignReadSerializer
    permission_classes = [AllowAny]
