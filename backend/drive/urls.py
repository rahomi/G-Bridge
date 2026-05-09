from django.urls import path

from .views import HealthCheckView, UploadDriveFileView

urlpatterns = [
    path("upload/", UploadDriveFileView.as_view(), name="upload-drive-file"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
