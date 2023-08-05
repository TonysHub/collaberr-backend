from django.urls import path
from core.api.creators.views import (
        request_to_join_campaign,
        CreatorStatsView,
        CreatorListAPIView,
    )


urlpatterns = [
    path('creator/', CreatorListAPIView.as_view()),
    path('creator/join-campaign/', request_to_join_campaign),
    path('creator/stats/', CreatorStatsView.as_view()),
]
