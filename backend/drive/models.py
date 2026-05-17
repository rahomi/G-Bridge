from django.db import models


class DriveFile(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(blank=True, default="")
    file_name = models.CharField(max_length=255, blank=True, default="")
    google_drive_id = models.CharField(max_length=255, blank=True, default="")
    web_view_link = models.URLField(blank=True, default="")
    web_content_link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        label = self.title or self.file_name or "Drive file"
        drive_id = self.google_drive_id or "n/a"
        return f"{label} ({drive_id})"
