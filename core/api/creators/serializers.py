from rest_framework import serializers
from .models import Creator


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'
