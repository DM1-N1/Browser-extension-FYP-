// Configure the backend URL(s) for the extension.
// The extension will try localhost first, then any configured remote URL.

const LOCAL_SERVER_URL = 'http://127.0.0.1:5000'
const LOCALHOST_SERVER_URL = 'http://localhost:5000'

// If you run the backend in Codespace, set CODESPACE_SERVER_URL to the forwarded URL.
// Example:
// const CODESPACE_SERVER_URL = 'https://<your-codespace-id>-5000.preview.app.github.dev'
const CODESPACE_SERVER_URL = ''

function getServerUrls() {
    const urls = [LOCAL_SERVER_URL, LOCALHOST_SERVER_URL]
    if (CODESPACE_SERVER_URL) {
        urls.push(CODESPACE_SERVER_URL)
    }
    return urls
}
