import requests
import os

# The URL where the Flask server is running
api_url = os.getenv('PREDICTION_URL', 'http://127.0.0.1:5000/predict')

# URL to test the backend with
test_url = 'https://www.example.com/'

# Create the data payload for the current Flask endpoint
payload = {
    'url': test_url
}

try:
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        prediction = response.json()
        print(f'Prediction for {test_url}: {prediction}')
    else:
        print(f'Error: {response.status_code}, Response: {response.text}')
except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

