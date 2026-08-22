import requests

# The url where the Flask server is running
url = 'http://127.0.0.1:5000/predict'

test_url = 'https://www.google.com/'

data = {
    'url': test_url
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        prediction = response.json()
        print(f'Prediction for {test_url}: {prediction}')
    else:
        print(f'Error: {response.status_code}, Response: {response.text}')
except requests.exceptions.RequestException as e:
    print(f'Could not connect to the Flask server. Make sure it is running. Details: {e}')

