import os
import google.oauth2.credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'


class YoutubeQueryHook:
    """
    Plugin to retrieve Youtube Report for User
    Ex. youtube_hook = YoutubeQueryHook(**credentials)
        query_result = hook.get_query(**query_param)
    """
    def __init__(self, **kwargs):
        self.service = self.get_service(**kwargs)

    def get_service(self, **kwargs):
        """
        credentials = {
        'key': YOUTUBE_ACCESS_TOKEN,
        'client_id': YOUTUBE_CLIENT_ID,
        'client_secret': YOUTUBE_CLIENT_SECRET,
        'refresh_token': YOUTUBE_REFRESH_TOKEN
        }
        """
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            {
                'key': kwargs.get('key'),
                'client_id': kwargs.get('client_id'),
                'client_secret': kwargs.get('client_secret'),
                'refresh_token': kwargs.get('refresh_token'),
            },
            scopes=SCOPES
        )
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def remove_empty_kwargs(**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if value:
                    good_kwargs[key] = value
        return good_kwargs

    def execute_api_request(self, client_library_function, **kwargs):
        response = client_library_function(**kwargs).execute()
        return response

    def get_query(self, **kwargs):
        """
        query_params = {
        'channel_id': '',
        'start_date': '2022-01-01',
        'end_date': '2022-01-20',
        'metrics': 'views',
        'dimensions': 'day',
        'sort': 'day',
        }
        """
        # SECURITY WARNING: Disable in production
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        response = self.execute_api_request(
            self.service.reports().query,
            ids='channel==' + kwargs.get('channel_id'),
            startDate=kwargs.get('start_date'),
            endDate=kwargs.get('end_date'),
            metrics=kwargs.get('metrics'),
            dimensions=kwargs.get('dimensions'),
            sort=kwargs.get('sort'),
        )
        return response
