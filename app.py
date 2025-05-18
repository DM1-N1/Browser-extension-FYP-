# This code creates a server using for flask which listens for post requests on the /predict route. 
# When a request is received, it calls the predict function and returns the prediction as a JSON response.
# Was very hard for me to understand but I got there in the end 




from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from feature_extractorv3 import extract_features_super

app = Flask(__name__)
CORS(app)

# Load the traditional ML model
model = joblib.load("ai_model.pkl")  # Your .pkl file

# Define the expected feature order (must match training)
feature_order = ['length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_at',
       'nb_qm', 'nb_and', 'nb_or', 'nb_eq', 'nb_underscore', 'nb_tilde',
       'nb_percent', 'nb_slash', 'nb_star', 'nb_colon', 'nb_comma',
       'nb_semicolumn', 'nb_dollar', 'nb_space', 'nb_www', 'nb_com',
       'nb_dslash', 'http_in_path', 'https_token', 'ratio_digits_url',
       'ratio_digits_host', 'punycode', 'port', 'tld_in_path',
       'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains',
       'prefix_suffix', 'random_domain', 'shortening_service',
       'length_words_raw', 'char_repeat', 'shortest_word_host',
       'shortest_word_path', 'longest_words_raw', 'longest_word_host',
       'longest_word_path', 'avg_words_raw', 'avg_word_host', 'avg_word_path',
       'phish_hints', 'domain_in_brand', 'brand_in_subdomain', 'brand_in_path',
       'suspecious_tld', 'statistical_report', 'nb_hyperlinks',
       'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks',
       'nb_extCSS', 'ratio_intRedirection', 'ratio_extRedirection',
       'ratio_intErrors', 'ratio_extErrors', 'links_in_tags', 'ratio_intMedia',
       'ratio_extMedia', 'popup_window', 'safe_anchor', 'onmouseover',
       'right_clic', 'empty_title', 'url_numeric_path_length',
       'url_numeric_num_subdomains', 'url_numeric_has_ip',
       'url_numeric_has_special_chars']


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url", "")
    print("Received data:", data)

    try:
        features = extract_features_super(url)
        print("Extracted features:", features)

        feature_list = [float(features.get(key, 0)) for key in feature_order]
        print("Feature list:", feature_list)

        # Predict using the traditional model
        prediction = model.predict([feature_list])[0]
        probabilities = model.predict_proba([feature_list])[0]
        confidence = max(probabilities)
        print("Predicted class:", prediction)
        print("Confidence level:", confidence)

        return jsonify({"prediction": int(prediction),"confidence": float(confidence)})

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

