from report import YoutubeReportHook
import logging
import time
from django.conf import settings

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
    data_dir = settings.BASE_DIR / download_path
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
        time.sleep(5)
