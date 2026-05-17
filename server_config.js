// Configure the backend URL(s) for the extension.
// The extension will try the most specific configured server URL first, then fallback to local host.

const LOCAL_SERVER_URL = 'http://127.0.0.1:5000'
const LOCALHOST_SERVER_URL = 'http://localhost:5000'

// If your backend runs in a GitHub Codespace, set CODESPACE_SERVER_URL to the forwarded preview URL.
// Example:
// const CODESPACE_SERVER_URL = 'https://<your-codespace-id>-5000.preview.app.github.dev'
const CODESPACE_SERVER_URL = ''

// Add any extra backend endpoints you want the extension to try.
const ADDITIONAL_SERVER_URLS = [
    // 'https://example.com/predict-backend'
]

function getServerUrls() {
    const urls = [
        ...[CODESPACE_SERVER_URL].filter(Boolean),
        ...ADDITIONAL_SERVER_URLS.filter(Boolean),
        LOCAL_SERVER_URL,
        LOCALHOST_SERVER_URL,
    ]
    return Array.from(new Set(urls))
}
