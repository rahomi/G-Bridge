from django.contrib import admin

from .models import DriveFile


@admin.register(DriveFile)
class DriveFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "google_drive_id", "uploaded_at")
    search_fields = ("file_name", "google_drive_id")
