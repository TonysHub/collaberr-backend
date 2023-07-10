import requests
from urllib.parse import urlencode, parse_qs, urlparse
# django imports
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
# drf imports
from rest_framework.views import APIView
# google imports
from google_auth_oauthlib.flow import Flow
# collaberr imports
from core.api.youtube_analytics.serializers import YoutubeCredentialsSerializer
from core.api.creators.models import Creator
import logging

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
REDIRECT_URI = "http://localhost:8000/api/youtube/oauth2callback/"

logger = logging.getLogger(__name__)


class YoutubeAuthView(APIView):
    """
    Pass in Collaberr Auth redirect URL to frontend
    """
    def get(self, request):
        if request.user.is_authenticated:
            flow = Flow.from_client_secrets_file(
                settings.YOUTUBE_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            return JsonResponse({'authorization_url': authorization_url})
        else:
            return HttpResponseForbidden('Access denied')

    def patch(self, request):
        """
        After user has authorized Collaberr,
        pass in channel_id and channel_name and
        redirect url to frontend
        """
        if request.user.is_authenticated:
            flow = Flow.from_client_secrets_file(
                settings.YOUTUBE_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            account_id = request.user.id
            try:
                creator = Creator.objects.get(account_id=account_id)
                creator.channel_handle = request.data['channel_handle']
                # creator.channel_id = request.data['channel_id']
                # creator.channel_name = request.data['channel_name']
                creator.save()
            except Creator.DoesNotExist:
                JsonResponse({'error': 'Creator does not exist'})

            return JsonResponse({'authorization_url': authorization_url})
        else:
            return HttpResponseForbidden('Access denied')


class YoutubeCallbackView(APIView):
    """
    Ask for OAuth2 token from Google
    """
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.YOUTUBE_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        logger.info(request.user)
        logger.info(request.user.is_authenticated)

        credentials = flow.credentials
        redirect_url = 'http://localhost:8000/api/youtube/confirm/?' + urlencode({
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scope': credentials.scopes[0],
        })

        response = HttpResponseRedirect(redirect_url)
        return response


class YoutubeConfirmView(APIView):
    """
    Store OAuth2 token in database
    """
    # SECURITY WARNING, Don't pass in through URL and need authentication!
    def get(self, request):
        url = request.build_absolute_uri()
        url_components = urlparse(url)
        params = parse_qs(url_components.query)
        params = {key: value[0] for key, value in params.items()}
        logger.info(params)
        logger.info(request.user.is_authenticated)

        serializer = YoutubeCredentialsSerializer(data=params, context={'request': request})
        creator = Creator.objects.get(account_id=request.user.id)
        if serializer.is_valid(raise_exception=True):
            if creator.verify_channel(**serializer.validated_data):
                serializer.save()
            return redirect('http://localhost:3000/youtubeConfirm/')
        return HttpResponseBadRequest('Invalid parameters')


class YoutubeRevokeView(APIView):
    def get(self, request):
        revoke_url = 'https://oauth2.googleapis.com/revoke'
        params = {'token': ''}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(revoke_url, params=params, headers=headers)

        if response.status_code == 200:
            return HttpResponse('Successfully disconnected')
        else:
            return HttpResponseBadRequest('Failed to disconnect Youtube account')
