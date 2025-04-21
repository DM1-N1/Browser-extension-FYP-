from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

#This part loads the models and the features
model = joblib.load("C:/Users/user/OneDrive/Desktop/Software engineering/Third year L6/Browser-extension-FYP-/ai_model.pkl")
features = joblib.load("C:/Users/user/OneDrive/Desktop/Software engineering/Third year L6/Browser-extension-FYP-/features.pkl")
@app.route("/predict", methods=["POST"])

def prediction():
    data = request.get_json()
    
    try:
        # Expecting features as a list: [path_length, num_subdomains, has_ip, uses_https, has_special_chars]
        input_features = np.array(data['features']).reshape(1, -1)

        # You must manually add placeholder values or pre-fill the other features
        # Example: [0,0,0,...,last 5 features]
        full_feature_vector = [0]*88 + input_features.flatten().tolist()  # 88 features before your 5 custom ones

        prediction = model.predict([full_feature_vector])[0]
        return jsonify({'prediction': int(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})

# Need this part below if running in a repository
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)