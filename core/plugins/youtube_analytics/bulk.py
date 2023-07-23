import dotenv
import os
import logging
import time

from pathlib import Path
import boto3

from report import YoutubeReportHook
from botocore.exceptions import ClientError

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


def bulk_download_report(credentials, download_path):
    """
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / 'data'

    bulk_download_report(
        credentials,
        download_path=data_dir
    )
    """
    yt_report_hook = YoutubeReportHook(**credentials)
    job_info = yt_report_hook.list_reporting_jobs()
    report_info = []
    for job in job_info:
        job_id = job['id']
        report_url_info = yt_report_hook.retrieve_reports(job_id=job_id)
        for report_url in report_url_info:
            report_info.append({
                'job_id': job_id,
                'name': job['name'],
                'report_type': job['report_type'],
                'report_url': report_url['report_url'],
                'start_time': report_url['start_time'],
                'end_time': report_url['end_time'],
            })
    for report in report_info:
        yt_report_hook.download_report(
            report_url=report['report_url'],
            local_file=f'{data_dir}/{report["report_type"]}/{report["start_time"][:10]}.csv'
        )
        time.sleep(15)


def bulk_upload_directory(directory, bucket, prefix=''):
    """Upload all files in a directory to an S3 bucket

    :param directory: Directory to upload files from
    :param bucket: Bucket to upload to
    :param prefix: Channel ID
    :return: True if all files were uploaded, else False
    """
    print(f'Uploading {directory} to {bucket}/{prefix}')

    # Create an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )

    # Iterate through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.join(prefix, os.path.relpath(file_path, directory))

            try:
                s3_client.upload_file(file_path, bucket, object_name)
                print(f'Uploaded {file_path} to {bucket}/{object_name}')
            except ClientError as e:
                logging.error(e)
                return False

    return True


# base_dir = Path(__file__).resolve().parent.parent.parent.parent
# data_dir = base_dir / 'data'

# bulk_upload_directory(
#     directory=data_dir,
#     bucket='collaberr',
#     prefix='youtube_reports/UCvL8YftvoKcb_XPUHBCh8hw'
# )
