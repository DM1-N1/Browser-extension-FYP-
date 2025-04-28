import requests

# The URL where the Flask server is running
url = 'http://127.0.0.1:5000/predict'

# Define the features as a dictionary (ensure these match the order of your model's expected input)
features = [
    37, 19, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0.0, 0.0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 4, 4, 3, 3, 3, 11, 11, 6, 5.75, 7.0, 4.5, 0, 0, 0, 0, 0, 0, 17, 0.529411765, 0.470588235, 0, 0, 0, 0.875, 0, 0.5, 0, 0, 80.0, 0, 100.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 1, 0, 45, -1, 0, 1, 1, 4, 5135, 11, 1, 0, 0
]

# Create the data payload to send in the POST request
data = {
    'features': features
}

try:
    # Send POST request to Flask API
    response = requests.post(url, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        prediction = response.json()
        print(f'Prediction: {prediction["prediction"]}')
    else:
        # Print error details if the response is not successful
        print(f'Error: {response.status_code}, Response: {response.json()}')

except requests.exceptions.RequestException as e:
    # Handle connection errors or other request exceptions
    print(f'An error occurred: {e}')

