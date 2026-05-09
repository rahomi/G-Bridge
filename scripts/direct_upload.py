import os
import sys
import django
import io

# Load .env into os.environ
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

# Ensure Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Add project root to path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# Also add backend package directory explicitly to ensure backend.settings is importable
BACKEND_PATH = os.path.join(ROOT, 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

try:
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    raise

from drive.services import upload_file_to_drive
from drive.models import DriveFile

TEST_FILE = os.path.join(ROOT, 'test_upload.txt')

class FileLike:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.content_type = 'text/plain'
    def read(self):
        with open(self.path, 'rb') as f:
            return f.read()

if not os.path.exists(TEST_FILE):
    print('Test file not found:', TEST_FILE)
    sys.exit(2)

u = FileLike(TEST_FILE)
print('Uploading', u.name)

try:
    result = upload_file_to_drive(u)
    print('Drive API response:')
    print(result)

    drive_file = DriveFile.objects.create(
        file_name=result.get('name', u.name),
        google_drive_id=result['id'],
        web_view_link=result.get('webViewLink', ''),
        web_content_link=result.get('webContentLink', ''),
    )
    print('Saved DriveFile id:', drive_file.id)
    print('web_view_link:', drive_file.web_view_link)
except Exception as exc:
    print('Upload failed:', type(exc).__name__, exc)
    raise
