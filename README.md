# Telegram to Google Drive PDF Sync 📂 🚀

An asynchronous Python automation script that extracts PDF documents from a specific Telegram channel and securely backs them up to a Google Drive folder. 

This tool is designed to be lightweight and storage-efficient. It downloads files locally, tracks the transfer with visual progress bars, streams the upload to Google Drive in chunks, and automatically deletes the local copy once the upload is verified.

## ✨ Features

* **Asynchronous Operations:** Built with `Telethon` and `asyncio` for efficient Telegram message parsing and media downloading.
* **Smart Filtering:** Automatically scans the channel history and strictly targets `application/pdf` MIME types.
* **Visual Progress Tracking:** Features custom CLI progress bars (`[██████████----------] 50.0%`) for both the Telegram download and the Google Drive upload phases.
* **Chunked Uploads:** Uploads to Google Drive using 2MB chunks (`resumable=True`), making it stable for larger PDF files.
* **Zero Storage Footprint:** Automatically cleans up (deletes) the local PDF file immediately after a successful upload to Drive.
* **First-Run Auth:** Automatically handles Google Drive OAuth2 flow and generates a reusable `token.json` for subsequent background runs.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed and set up:

* **Python 3.7+**
* A Telegram account to generate API credentials.
* A Google account to generate Drive API credentials.

### 1. Get Telegram API Credentials
1. Log in to your Telegram core portal: [https://my.telegram.org/](https://my.telegram.org/)
2. Go to **API development tools**.
3. Create a new application to get your `api_id` and `api_hash`.

### 2. Get Google Drive API Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Drive API**.
3. Go to **Credentials** -> **Create Credentials** -> **OAuth client ID** (Choose "Desktop App").
4. Download the JSON file and rename it to `credentials.json`.
5. Place `credentials.json` in the root directory of this project.

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/telegram-to-drive-sync.git
cd telegram-to-drive-sync
```

**2. Create a virtual environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
Install the required packages using pip. 
```bash
pip install telethon google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**4. Configuration**
Open `telegram_to_drive.py` (or your script name) and update the configuration variables at the top of the file with your specific details:

```python
# --- YOUR CONFIGURATION ---
API_ID = 12345678                  # Replace with your Telegram API ID (integer)
API_HASH = 'your_api_hash_here'    # Replace with your Telegram API Hash (string)
CHANNEL_USERNAME = '@your_channel' # Replace with the target Telegram channel username
DRIVE_FOLDER_ID = 'your_folder_id' # Replace with your target Google Drive Folder ID
```

## 💻 Usage

Run the script from your terminal:

```bash
python3 telegram_to_drive.py
```

### What to expect on the first run:
1. **Google Auth:** A browser window will open asking you to authorize the application to access your Google Drive. Once accepted, a `token.json` file will be created locally so you don't have to log in again.
2. **Telegram Auth:** The terminal will prompt you to enter your Telegram phone number and the login code sent to your Telegram app. This creates a `.session` file.
3. **Execution:** The script will scan the channel, download PDFs, and stream them to your Drive.

## ⚠️ Important Notes
* **Security:** **Never** commit your `credentials.json`, `token.json`, or Telegram session files to GitHub. Ensure they are added to your `.gitignore` file.
* **Rate Limits:** Be mindful of Telegram's download limits and Google Drive's API quotas if you are parsing a channel with thousands of heavy PDFs.

## 📜 License
[MIT License](LICENSE)
