# This code creates a server using for flask which listens for post requests on the /predict route. 
# When a request is received, it calls the predict function and returns the prediction as a JSON response.
# Was very hard for me to understand but I got there in the end 
import joblib
from flask import Flask, request, jsonify
from feature_extractor import extract_features

# order of features used in the model 
model_order = [
    'length_url','length_hostname','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq',
    'nb_underscore','nb_tilde','nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn',
    'nb_dollar','nb_space','nb_www','nb_com','http_in_path','ratio_digits_url',
    'ratio_digits_host','punycode','port','tld_in_path','tld_in_subdomain','abnormal_subdomain',
    'prefix_suffix','random_domain','shortening_service','path_extension','nb_redirection','nb_external_redirection',
    'shortest_words_raw','shortest_word_path','longest_words_raw','longest_word_host','longest_word_path',
    'phish_hints','domain_in_brand','brand_in_subdomain','brand_in_path','suspecious_tld','statistical_report',
    'nb_hyperlinks','ratio_intHyperlinks','ratio_extHyperlinks','ratio_nullHyperlinks','nb_extCSS',
    'ratio_intRedirection','ratio_extRedirection','ratio_intErrors','ratio_extErrors','login_form','external_favicon',
    'links_in_tags','submit_email','ratio_intMedia','ratio_extMedia','sfh','iframe','popup_window','safe_anchor',
    'onmouseover','right_clic','empty_title','domain_with_copyright','google_index','page_rank',
    'url_numeric_domain','url_numeric_path_length','url_numeric_num_subdomains','url_numeric_has_ip',
    'url_numeric_has_special_chars'
]

model = joblib.load("ai_model.pkl")  
print(model.n_features_in_)


# Initialize Flask app
app = Flask(__name__)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'})
        feature_dictionary = extract_features(url)
        #convert the feature dictionary to a list to be safe 


        missing_features = [feature for feature in model_order if feature not in feature_dictionary]
        if missing_features:
            return jsonify({'error': f'Missing features: {missing_features}'})

        feature_list = [feature_dictionary[feature] for feature in model_order]
        

        # features = data.get('features')

        # if not features:
        #     return jsonify({'error': 'No features provided'})
        
        # # print("Received features:", features)
        # print("Recieved Features)")
        
        
        if len(feature_list) != model.n_features_in_:
            return jsonify({'error': f"Expected {model.n_features_in_} features, but got {len(feature_list)}"})

        # Predict with the model
        prediction = model.predict([feature_list])
        return jsonify({'prediction': int(prediction[0])})
        
    except Exception as e:
        return jsonify({'error': str(e)})


# Run the app
if __name__ == "__main__":
    app.run(debug=True)  

