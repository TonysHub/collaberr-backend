from django.urls import path
from core.api.creators.views import request_to_join_campaign, CreatorStatsView


urlpatterns = [
    path('creator/join-campaign/', request_to_join_campaign),
    path('creator/stats/', CreatorStatsView.as_view()),
]
