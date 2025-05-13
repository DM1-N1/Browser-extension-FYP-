import joblib
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model  # type: ignore
from feature_extractor import extract_features  # Import the feature extraction function

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = load_model('deeplearn.keras')  # Load the saved model
# Load the scaler used for feature scaling
scaler = joblib.load("deep_scaler.pkl")  # Load the scaler

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Extract URL from the input
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'})

        # Extract features from the URL using the feature_extractor
        extracted_features = extract_features(url)
        
        # Collect features into a list for prediction
        feature_list = [
            extracted_features['length_url'],
            extracted_features['nb_dots'],
            extracted_features['nb_hyphens'],
            extracted_features['nb_at'],
            extracted_features['nb_qm'],
            extracted_features['nb_and'],
            extracted_features['nb_or'],
            extracted_features['nb_eq'],
            extracted_features['nb_underscore'],
            extracted_features['nb_tilde'],
            extracted_features['nb_percent'],
            extracted_features['nb_slash'],
            extracted_features['nb_star'],
            extracted_features['nb_colon'],
            extracted_features['nb_comma'],
            extracted_features['nb_semicolumn'],
            extracted_features['nb_dollar'],
            extracted_features['nb_space'],
            extracted_features['nb_www'],
            extracted_features['nb_com'],
            extracted_features['nb_dslash'],
            extracted_features['http_in_path'],
            extracted_features['https_token'],
            extracted_features['punycode'],
            extracted_features['nb_subdomains'],
            extracted_features['url_numeric_path_length'],
            extracted_features['url_numeric_domain'],
        ]
        
        # Ensure the feature list has the same length as expected by the model
        expected_length = model.input_shape[1]
        print("hello", expected_length)
        if len(feature_list) != expected_length:
            return jsonify({'error': f"Expected {expected_length} features, but got {len(feature_list)}"})
        
        # Scale the features using the loaded scaler
        feature_list_scaled = scaler.transform([feature_list])
        
        # Predict with the model
        prediction = model.predict(feature_list_scaled)
        
        # Return the prediction result (convert prediction to binary class: 0 or 1)
        return jsonify({'prediction': int(prediction[0] > 0.5)})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
