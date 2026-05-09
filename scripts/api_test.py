import os
import sys
import django
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

# Ensure test client host is allowed
allowed_hosts = os.environ.get('ALLOWED_HOSTS', '')
if 'testserver' not in allowed_hosts:
    combined = ','.join([h for h in [allowed_hosts, 'testserver'] if h])
    os.environ['ALLOWED_HOSTS'] = combined

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
BACKEND_PATH = os.path.join(ROOT, 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)


django.setup()

client = Client()

print('Health check:')
health = client.get('/api/health/')
print('status', health.status_code)
try:
    print('body', health.json())
except Exception:
    print('body', health.content.decode('utf-8', errors='ignore'))

print('Upload test:')
file_path = os.path.join(ROOT, 'test_upload.txt')
with open(file_path, 'rb') as f:
    upload = SimpleUploadedFile('test_upload.txt', f.read(), content_type='text/plain')
    response = client.post('/api/upload/', {'file': upload})

print('status', response.status_code)
try:
    print(response.json())
except Exception:
    print(response.content.decode('utf-8', errors='ignore'))
