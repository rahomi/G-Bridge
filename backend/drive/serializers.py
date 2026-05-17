from rest_framework import serializers

from .models import DriveFile


class DriveFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveFile
        fields = [
            "id",
            "title",
            "description",
            "file_name",
            "google_drive_id",
            "web_view_link",
            "web_content_link",
            "uploaded_at",
        ]
