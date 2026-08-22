# Browser-extension-FYP-

This is a browser extension that uses AI to detect whether a site is legitimate or not. It was developed as my final year project.

## Features
- AI-powered detection of legitimate and fraudulent websites.
- Real-time analysis of website content and metadata.
- User-friendly interface with alerts and recommendations.
- Lightweight and easy to install.

## Installation
1. Clone this repository

2. Install Python dependencies in the repository environment:
   - `python3 -m pip install -r requirements.txt`

3. Start the Flask backend from the repository root:
   - `source venv/bin/activate && python app.py`

4. Open your browser and navigate to the extensions page:
   - For Chrome: `chrome://extensions/`
5. Enable "Developer mode."
6. Click "Load unpacked" and select the cloned repository folder.

## Notes for Codespaces
- If the backend runs inside a Codespace, the extension cannot use `http://127.0.0.1:5000` from your browser.
- Set `CODESPACE_SERVER_URL` in `server_config.js` to the forwarded preview URL for your Codespace.
- Example:
  - `const CODESPACE_SERVER_URL = 'https://<your-codespace-id>-5000.preview.app.github.dev'`

## Usage
1. Once installed and the backend is running, open the extension popup.
2. The popup will try the local Flask server first, then the configured Codespace backend if provided.
3. If the extension still says "Error fetching prediction," check the browser console and confirm the backend is reachable.



