from rest_framework import serializers
from .models import Song
from datetime import datetime
from django.utils import timezone

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'name', 'duration', 'uploaded_time', 'audio_file']

    def validate_uploaded_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Uploaded time cannot be in the past.")
        return value

    def validate_audio_file(self, value):
        allowed_types = ['audio/mpeg', 'audio/wav', 'audio/x-ms-wma', 'audio/amr']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Invalid file type. Allowed types are: mp3, wav, wma, amr.")
        return value
