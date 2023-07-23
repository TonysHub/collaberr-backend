import os
import boto3
import dotenv
import csv

from django.core.management.base import BaseCommand

from core.api.youtube_analytics.models import YoutubeChannelBasic
from core.api.youtube_analytics.serializers import YoutubeChannelBasicSerializer
from core.api.creators.models import Creator

dotenv.load_dotenv()


class Command(BaseCommand):
    help = 'Import data from CSV files in S3 to PostgreSQL'

    def handle(self, *args, **options):
        channel_id = 'UCvL8YftvoKcb_XPUHBCh8hw'
        bucket_name = 'collaberr'
        s3_folder_name = f'youtube_reports/{channel_id}/channel_basic_a2/'
        local_temp_directory = '/tmp'

        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        try:
            # Retrieve the list of CSV files in the S3 folder
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder_name)
            csv_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
            creator = Creator.objects.get(channel_id=channel_id)

            # Download CSV files to the local temporary directory
            for csv_file in csv_files:
                with open(os.path.join(local_temp_directory, os.path.basename(csv_file)), 'r') as f:
                    # Deserialize the CSV data using the serializer
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Add Creator details to each row of CSV data
                        row['creator_id'] = creator.id
                        row['owner'] = creator.account_id.id
                        row['channel_handle'] = creator.channel_handle
                        row['channel_name'] = creator.channel_name
                        subscribed_mapping = {'subscribed': True, 'not_subscribed': False}

                        row['subscribed_status'] = subscribed_mapping.get(row['subscribed_status'], False)

                        serializer = YoutubeChannelBasicSerializer(data=row)
                        if serializer.is_valid():
                            serializer.save()
                            print(f"Data from {csv_file} saved to {YoutubeChannelBasic._meta.db_table}")
                        else:
                            print(f"Invalid data from {csv_file}: {serializer.errors}")

            print("Data copying completed.")
        except Exception as e:
            print(f"Error: {e}")
