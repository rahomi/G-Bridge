from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DriveFile
from .serializers import DriveFileSerializer
from .services import (
    delete_file_from_drive,
    replace_file_in_drive,
    upload_file_to_drive,
)


class UploadDriveFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        title = request.data.get("title", "")
        description = request.data.get("description", "")

        drive_metadata = None
        if uploaded_file:
            try:
                drive_metadata = upload_file_to_drive(uploaded_file)
            except Exception as exc:
                return Response(
                    {"detail": str(exc)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        drive_file = DriveFile.objects.create(
            title=title,
            description=description,
            file_name=(
                drive_metadata.get("name", uploaded_file.name)
                if drive_metadata and uploaded_file
                else ""
            ),
            google_drive_id=drive_metadata["id"] if drive_metadata else "",
            web_view_link=drive_metadata.get("webViewLink", "") if drive_metadata else "",
            web_content_link=drive_metadata.get("webContentLink") if drive_metadata else None,
        )

        serializer = DriveFileSerializer(drive_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DriveFileListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        drive_files = DriveFile.objects.order_by("-uploaded_at")
        serializer = DriveFileSerializer(drive_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        upload_view = UploadDriveFileView()
        return upload_view.post(request)


class DriveFileDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, file_id):
        drive_file = get_object_or_404(DriveFile, id=file_id)
        serializer = DriveFileSerializer(drive_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, file_id):
        drive_file = get_object_or_404(DriveFile, id=file_id)
        title = request.data.get("title")
        description = request.data.get("description")
        uploaded_file = request.FILES.get("file")

        if title is not None:
            drive_file.title = title
        if description is not None:
            drive_file.description = description

        if uploaded_file:
            try:
                if drive_file.google_drive_id:
                    drive_metadata = replace_file_in_drive(
                        drive_file.google_drive_id,
                        uploaded_file,
                    )
                else:
                    drive_metadata = upload_file_to_drive(uploaded_file)
            except Exception as exc:
                return Response(
                    {"detail": str(exc)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            drive_file.file_name = drive_metadata.get("name", uploaded_file.name)
            drive_file.web_view_link = drive_metadata.get("webViewLink", "")
            drive_file.web_content_link = drive_metadata.get("webContentLink")
            drive_file.google_drive_id = drive_metadata.get("id", drive_file.google_drive_id)

        drive_file.save()
        serializer = DriveFileSerializer(drive_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, file_id):
        return self.patch(request, file_id)

    def delete(self, request, file_id):
        drive_file = get_object_or_404(DriveFile, id=file_id)
        if drive_file.google_drive_id:
            try:
                delete_file_from_drive(drive_file.google_drive_id)
            except Exception as exc:
                return Response(
                    {"detail": str(exc)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        drive_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
