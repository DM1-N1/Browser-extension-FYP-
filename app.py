

# @app.route('/predict', methods=['POST'])
# def predict():
#         try:
#             data = request.get_json(force=True)
#             features = data.get('features')

#             if not features:
#                 return jsonify({'error': 'No features provided'}), 400

#             prediction = model.predict([features])
#             print("All good")
#             return jsonify({'prediction': int(prediction[0])})

#         except Exception as e:
#             return jsonify({'error': str(e)}), 500


# === Imports ===
import joblib
from flask import Flask, request, jsonify

# Load the trained model (make sure the model file is in the same directory)
model = joblib.load("ai_model.pkl")  # Change to your model's filename

print(model.n_features_in_)


# Initialize Flask app
app = Flask(__name__)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        features = data.get('features')

        if not features:
            return jsonify({'error': 'No features provided'}), 400
        
        print("Received features:", features)  # Print to see the features
        
        # Check length
        print(f"Number of features received: {len(features)}")
        
        if len(features) != model.n_features_in_:
            return jsonify({'error': f"Expected {model.n_features_in_} features, but got {len(features)}"}), 400

        # Predict with the model
        prediction = model.predict([features])
        
        print("All good")
        return jsonify({'prediction': int(prediction[0])})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Run the app
if __name__ == "__main__":
    app.run(debug=True)  # Starts the server on http://127.0.0.1:5000

