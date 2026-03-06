#!/usr/bin/env python3
"""
YouTube Auto Uploader
Uploads videos automatically to FutureFables AI channel
"""

import os
import json
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.pickle"

def get_youtube_service():
    """Get authenticated YouTube service."""
    creds = None

    # Load saved token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    # Refresh or get new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save token
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def upload_video(video_path: str, title: str, description: str,
                 tags: list, category_id: str = "28",
                 privacy: str = "public") -> dict:
    """
    Upload video to YouTube.
    Category IDs: 28=Science&Tech, 22=People&Blogs, 25=News
    """
    try:
        youtube = get_youtube_service()

        body = {
            "snippet": {
                "title":       title[:100],  # YouTube max 100 chars
                "description": description,
                "tags":        tags[:500],
                "categoryId":  category_id,
                "defaultLanguage": "ta",
            },
            "status": {
                "privacyStatus":           privacy,
                "selfDeclaredMadeForKids": False,
            }
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024*1024*5  # 5MB chunks
        )

        print(f"📤 Uploading: {title}")
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   Upload progress: {progress}%")

        video_id  = response["id"]
        video_url = f"https://youtube.com/watch?v={video_id}"

        print(f"✅ Uploaded! URL: {video_url}")
        return {
            "success":   True,
            "video_id":  video_id,
            "video_url": video_url,
            "title":     title,
        }

    except Exception as e:
        print(f"❌ Upload error: {e}")
        return {"success": False, "error": str(e)}


def set_thumbnail(video_id: str, thumbnail_path: str):
    """Set custom thumbnail for video."""
    try:
        youtube = get_youtube_service()
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print(f"✅ Thumbnail set for {video_id}")
        return True
    except Exception as e:
        print(f"❌ Thumbnail error: {e}")
        return False


if __name__ == "__main__":
    print("🔐 Testing YouTube authentication...")
    print("A browser will open — login with your Google account!")
    print("Then come back to terminal.")
    youtube = get_youtube_service()
    print("✅ Authentication successful!")
    print("✅ YouTube uploader ready!")
