from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from core.api.creators.models import Creator
from core.api.creators.serializers import CreatorSerializer


class CreatorListAPIView(ListAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    permissions = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()
