// Get the original URL from the query parameter
let urlParams = new URLSearchParams(window.location.search);
let originalUrl = urlParams.get('url');

document.getElementById('proceed-button').addEventListener('click', () => {
    if (originalUrl) {
        window.location.href = originalUrl; // Redirect to the original URL
    } else {
        alert("Original URL not found.");
    }
});
