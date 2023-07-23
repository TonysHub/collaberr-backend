import logging
import boto3
from botocore.exceptions import ClientError
import os
import dotenv
from pathlib import Path

dotenv.load_dotenv()


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f'Uploaded {file_name} to {bucket}/{object_name}')
    except ClientError as e:
        logging.error(e)
        return False
    return True


base_dir = Path(__file__).resolve().parent.parent.parent.parent
data_dir = base_dir / 'data'

upload_file(
    file_name=f'{data_dir}/channel_basic_a2/2023-06-18.csv',
    bucket='collaberr'
)
