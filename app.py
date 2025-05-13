import joblib
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model  # type: ignore

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = load_model('ai_model.keras')  # Make sure to load your new Keras model file
scaler = joblib.load("scaler.pkl")  # Load the saved scaler

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'})

        # Assuming you've already converted the URL into the necessary numerical features
        # You should send the correctly preprocessed features, not raw URLs, to the model
        feature_list = data.get('features')  # This should be a list of features like [feature1, feature2, ...]

        if not feature_list:
            return jsonify({'error': 'No features provided'})

        # Ensure the feature list has the same length as expected by the model
        expected_length = model.input_shape[1]
        if len(feature_list) != expected_length:
            return jsonify({'error': f"Expected {expected_length} features, but got {len(feature_list)}"})

        # Scale the features using the loaded scaler
        feature_list_scaled = scaler.transform([feature_list])

        # Predict with the model
        prediction = model.predict(feature_list_scaled)

        # Return the prediction result
        return jsonify({'prediction': int(prediction[0] > 0.5)})  # Convert to binary class (0 or 1)

    except Exception as e:
        return jsonify({'error': str(e)})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
