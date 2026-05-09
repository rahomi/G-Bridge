from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DriveFile
from .serializers import DriveFileSerializer
from .services import upload_file_to_drive


class UploadDriveFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response(
                {"detail": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            drive_metadata = upload_file_to_drive(uploaded_file)
        except Exception as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        drive_file = DriveFile.objects.create(
            file_name=drive_metadata.get("name", uploaded_file.name),
            google_drive_id=drive_metadata["id"],
            web_view_link=drive_metadata.get("webViewLink", ""),
            web_content_link=drive_metadata.get("webContentLink"),
        )

        serializer = DriveFileSerializer(drive_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
