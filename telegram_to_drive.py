import os
import asyncio
from telethon import TelegramClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# --- YOUR CONFIGURATION ---
API_ID = 39960925
API_HASH = 'fcc06de795c3f4ec7e63f42701261895'
CHANNEL_USERNAME = '@hbr_uz'
DRIVE_FOLDER_ID = '1cP0iGC7ZlB-R_h3mxOdszf7g4cyJ1iqa'

# Scopes for Google Drive (Updated to full Drive access to prevent 404 errors)
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Authenticates with Google Drive and handles token creation."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, file_path):
    """Uploads the file in chunks and displays a progress bar."""
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [DRIVE_FOLDER_ID]
    }
    
    # resumable=True and chunksize allow us to track upload progress
    chunk_size = 2 * 1024 * 1024 # 2MB chunks
    media = MediaFileUpload(file_path, mimetype='application/pdf', resumable=True, chunksize=chunk_size)
    
    request = service.files().create(
        body=file_metadata, 
        media_body=media, 
        fields='id',
        supportsAllDrives=True 
    )
    
    print(f"   ☁️ Uploading to Drive...")
    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                # Calculate and draw the progress bar
                percent = status.progress() * 100
                bar_length = 40
                filled_length = int(bar_length * status.progress())
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f'\r   [{bar}] {percent:.1f}%', end='')
                
        # Print a new line and success message when it hits 100%
        print(f'\n   ✅ Successfully uploaded: {file_name}\n')
    except Exception as e:
        print(f'\n   ❌ Failed to upload {file_name}: {e}\n')

def download_progress(current, total):
    """Draws a visual progress bar for Telegram downloads."""
    if total:
        percent = (current / total) * 100
        bar_length = 40 
        filled_length = int(bar_length * current / total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f'\r   [{bar}] {percent:.1f}%', end='')
        
        if current == total:
            print() 

async def main():
    # Initialize Drive
    print("Initializing Google Drive service...")
    drive_service = get_drive_service()
    
    # Initialize Telegram
    print("Connecting to Telegram...")
    async with TelegramClient('hbr_sync_session', API_ID, API_HASH) as client:
        print(f"Scanning channel: {CHANNEL_USERNAME}...\n")
        
        # Iterating through messages
        async for message in client.iter_messages(CHANNEL_USERNAME):
            if message.document and message.document.mime_type == 'application/pdf':
                
                file_name = message.file.name if message.file.name else f"document_{message.id}.pdf"
                print(f"⬇️ Found: {file_name}")
                
                # Download with progress bar
                path = await message.download_media(progress_callback=download_progress)
                
                # Upload with progress bar
                upload_to_drive(drive_service, path)
                
                # Clean up local file
                if os.path.exists(path):
                    os.remove(path)
        
        print("✨ All PDFs have been processed!")

if __name__ == '__main__':
    asyncio.run(main())