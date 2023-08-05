import io
import os

import boto3
import dotenv
from PIL import Image

from django.db import models
from django.conf import settings

dotenv.load_dotenv()


def upload_thumbnail_to_s3(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    thumbnail_filename = f"{instance.title}-thumbnail{file_extension}"
    return f"{thumbnail_filename}"


class CampaignManager(models.Manager):
    def create_with_thumbnail(self, title, thumbnail_image, **kwargs):
        thumbnail_path = upload_thumbnail_to_s3(thumbnail_image, thumbnail_image.name)
        thumbnail_url = f's3://collaberr/campaigns/thumbnails/{thumbnail_path}'

        with Image.open(thumbnail_image) as img:
            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size)
            thumbnail_buffer = io.BytesIO()
            img.save(thumbnail_buffer, format='JPEG')
            thumbnail_buffer.seek(0)

            s3 = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
            s3.upload_fileobj(thumbnail_buffer, settings.AWS_BUCKET_NAME, thumbnail_path)

        return self.create(title=title, thumbnail_url=thumbnail_url, **kwargs)
