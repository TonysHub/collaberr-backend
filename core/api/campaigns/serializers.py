import io
import os

import dotenv
import boto3
import logging
from PIL import Image
from rest_framework import serializers

from .models import Campaign

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        # These fields are populated in models.py or create method
        read_only_fields = ['owner', 'created_at', 'modified_at', 'id', 'thumbnail_url']

    def create(self, validated_data):
        request = self.context.get('request')
        logging.info(f"Request: {request.FILES}")
        thumbnail_file = request.FILES['thumbnail']

        if thumbnail_file:
            # Generate and save the thumbnail to S3
            thumbnail_url = self.upload_thumbnail_to_s3(thumbnail_file, validated_data['title'])
            validated_data['thumbnail_url'] = thumbnail_url

        campaign = super().create({**validated_data, 'owner': request.user})
        return campaign

    def validate(self, data):
        data = super().validate(data)
        return data

    def upload_thumbnail_to_s3(self, thumbnail_file, title):

        with Image.open(thumbnail_file) as img:
            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size)
            thumbnail_buffer = io.BytesIO()
            # Save the resized image to the buffer in JPEG format
            img.save(thumbnail_buffer, format='JPEG')
            thumbnail_buffer.seek(0)

            filename = f'{title}-thumbnail.jpg'

            s3 = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
            s3.upload_fileobj(thumbnail_buffer, 'collaberr', filename)
            thumbnail_url = f's3://collaberr/campaigns/thumbnails/{filename}'
            logger.info(f"Thumbnail URL: {thumbnail_url}")

            return thumbnail_url



# Campaign Edit field which is only editable by owner

