# This code creates a server using for flask which listens for post requests on the /predict route. 
# When a request is received, it calls the predict function and returns the prediction as a JSON response.
# Was very hard for me to understand but I got there in the end 
import joblib
from flask import Flask, request, jsonify

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
            return jsonify({'error': 'No features provided'})
        
        # print("Received features:", features)
        print("Recieved Features)")
        
        
        if len(features) != model.n_features_in_:
            return jsonify({'error': f"Expected {model.n_features_in_} features, but got {len(features)}"})

        # Predict with the model
        prediction = model.predict([features])
        return jsonify({'prediction': int(prediction[0])})
        
    except Exception as e:
        return jsonify({'error':'Function did not work'})


# Run the app
if __name__ == "__main__":
    app.run(debug=True)  

