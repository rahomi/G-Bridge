from django.urls import path

from .views import (
    DriveFileDetailView,
    DriveFileListCreateView,
    HealthCheckView,
    UploadDriveFileView,
)

urlpatterns = [
    path("upload/", UploadDriveFileView.as_view(), name="upload-drive-file"),
    path("files/", DriveFileListCreateView.as_view(), name="drive-files"),
    path(
        "files/<int:file_id>/",
        DriveFileDetailView.as_view(),
        name="drive-file-detail",
    ),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
