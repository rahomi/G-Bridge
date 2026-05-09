from django.db import models


class DriveFile(models.Model):
    file_name = models.CharField(max_length=255)
    google_drive_id = models.CharField(max_length=255)
    web_view_link = models.URLField()
    web_content_link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.file_name} ({self.google_drive_id})"
