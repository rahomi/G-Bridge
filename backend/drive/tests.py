from django.test import TestCase

from .models import DriveFile
from .serializers import DriveFileSerializer


class DriveFileSerializerTests(TestCase):
    def test_serializer_outputs_expected_fields(self):
        drive_file = DriveFile.objects.create(
            title="Sample Title",
            description="Sample description",
            file_name="sample.txt",
            google_drive_id="drive-id",
            web_view_link="https://example.com/view",
            web_content_link="https://example.com/download",
        )

        serializer = DriveFileSerializer(drive_file)
        data = serializer.data

        self.assertEqual(data["title"], "Sample Title")
        self.assertEqual(data["description"], "Sample description")
        self.assertEqual(data["file_name"], "sample.txt")
        self.assertEqual(data["google_drive_id"], "drive-id")
        self.assertEqual(data["web_view_link"], "https://example.com/view")
        self.assertEqual(data["web_content_link"], "https://example.com/download")
        self.assertIn("uploaded_at", data)
