
import io
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

credentials = Credentials(
    token=None,
    refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    token_uri="https://oauth2.googleapis.com/token",
)
drive = build("drive", "v3", credentials=credentials)

FOLDER_ID = os.environ["GDRIVE_FOLDER_ID"]

def upload_pdf(filename, data):
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype="application/pdf")
    file = (
        drive.files().create(
            body={
                "name": filename,
                "parents": [FOLDER_ID],
            },
            media_body=media,
            fields="id"
        ).execute()
    )
    print(f"Uploaded {filename} to Google Drive folder {FOLDER_ID} (file id {file['id']})")