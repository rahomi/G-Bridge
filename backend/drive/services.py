import io
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise ValueError("Missing Google OAuth environment variables.")

    # When refreshing using a stored refresh token, avoid passing new scopes
    # (requesting new/expanded scopes on refresh can trigger `invalid_scope`).
    credentials = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    # Explicitly refresh to obtain an access token now and catch errors
    request = Request()
    try:
        credentials.refresh(request)
    except Exception as exc:
        # Surface a clearer error for caller
        raise RuntimeError(f"Failed to refresh Google credentials: {exc}") from exc

    return build("drive", "v3", credentials=credentials)


def upload_file_to_drive(uploaded_file):
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("Missing GOOGLE_DRIVE_FOLDER_ID environment variable.")

    service = get_drive_service()
    media = MediaIoBaseUpload(
        io.BytesIO(uploaded_file.read()),
        mimetype=uploaded_file.content_type,
        resumable=True,
    )
    file_metadata = {
        "name": uploaded_file.name,
        "parents": [folder_id],
    }

    created = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink, webContentLink",
        )
        .execute()
    )

    service.permissions().create(
        fileId=created["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return created


def replace_file_in_drive(google_drive_id, uploaded_file):
    service = get_drive_service()
    media = MediaIoBaseUpload(
        io.BytesIO(uploaded_file.read()),
        mimetype=uploaded_file.content_type,
        resumable=True,
    )
    file_metadata = {"name": uploaded_file.name}

    updated = (
        service.files()
        .update(
            fileId=google_drive_id,
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink, webContentLink",
        )
        .execute()
    )

    return updated


def delete_file_from_drive(google_drive_id):
    service = get_drive_service()
    service.files().delete(fileId=google_drive_id).execute()
