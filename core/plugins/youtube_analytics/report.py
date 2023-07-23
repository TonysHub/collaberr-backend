from io import FileIO
import logging
import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'

logger = logging.getLogger(__name__)


class YoutubeReportHook:
    """
    Plugin to retrieve Youtube Report for User
    Ex. yt_report_hook = YoutubeReportHook(**credentials)
        yt_report_hook.get_report_types()
        yt_report_hook.create_reporting_job('channel_traffic_source_a2', 'Traffic Source')
        yt_report_hook.list_reporting_jobs()
        yt_report_hook.retrieve_reports(job_id='')
        yt_report_hook.download_report(report_url='',
                                       local_file='')

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

    def get_report_types(self):
        """
        GET default report types
        """
        results = self.service.reportTypes().list().execute()
        reportTypes = results['reportTypes']

        if 'reportTypes' in results and results['reportTypes']:
            for reportType in reportTypes:
                print(f"Report type id: {reportType['id']} name: {reportType['name']}")
        else:
            print('No report types found')
            return False

        return True

    def create_reporting_job(self, report_type_id, report_name):
        """
        Select a desired report type and name
        """
        reporting_job = self.service.jobs().create(
            body=dict(
                reportTypeId=report_type_id,
                name=report_name,
            )
        ).execute()

        print('Reporting job "%s" created for reporting type "%s" at "%s"'
              % (reporting_job['name'], reporting_job['reportTypeId'], reporting_job['createTime']))

    def list_reporting_jobs(self):
        """
        List all jobs for the current account
        """
        results = self.service.jobs().list().execute()

        if 'jobs' in results and results['jobs']:
            jobs = results['jobs']
            job_info = []
            for job in jobs:
                print('Reporting job id: %s\n name: %s\n for reporting type: %s\n'
                      % (job['id'], job['name'], job['reportTypeId']))
                job_info.append({
                    "id": job['id'],
                    "name": job['name'],
                    "report_type": job['reportTypeId'],
                })
            return job_info
        else:
            print('No jobs found')
            return False

        return True

    def retrieve_reports(self, job_id):
        """
        Get reports within the job
        """
        try:
            results = self.service.jobs().reports().list(
                jobId=job_id,
                onBehalfOfContentOwner=''
            ).execute()
            if 'reports' in results and results['reports']:
                reports = results['reports']
                report_url_info = []
                for report in reports:
                    # print('Report times: %s to %s\n       download URL: %s\n'
                    #       % (report['startTime'], report['endTime'], report['downloadUrl']))
                    report_url_info.append({
                        "report_url": report['downloadUrl'],
                        "start_time": report['startTime'],
                        "end_time": report['endTime'],
                    })
                return report_url_info
            else:
                print("No reports found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def download_report(self, report_url, local_file):
        dir = os.path.dirname(local_file)

        # Create the dir if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        request = self.service.media().download(
            resourceName=' '
        )
        request.uri = report_url
        fh = FileIO(local_file, mode='wb')
        downloader = MediaIoBaseDownload(fh, request, chunksize=-1)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
        if status:
            print(f'Downloaded {local_file}')
            print('Download %d%%.' % int(status.progress() * 100))
        print('Download Complete!')

    def upload_to_s3(self, local_file):
        pass
