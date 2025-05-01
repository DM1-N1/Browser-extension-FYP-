import requests
from feature_extractor import extract_features

# The url where the Flask server is running
url = 'http://127.0.0.1:5000/predict'

test_url = 'http://bbc.com'

feature_dictionary = extract_features(test_url)

# order of features used in the model 
model_order = [
    'length_url','length_hostname','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq',
    'nb_underscore','nb_tilde','nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn',
    'nb_dollar','nb_space','nb_www','nb_com','nb_dslash','http_in_path','https_token','ratio_digits_url',
    'ratio_digits_host','punycode','port','tld_in_path','tld_in_subdomain','abnormal_subdomain','nb_subdomains',
    'prefix_suffix','random_domain','shortening_service','path_extension','nb_redirection','nb_external_redirection',
    'length_words_raw','char_repeat','shortest_words_raw','shortest_word_host','shortest_word_path',
    'longest_words_raw','longest_word_host','longest_word_path','avg_words_raw','avg_word_host','avg_word_path',
    'phish_hints','domain_in_brand','brand_in_subdomain','brand_in_path','suspecious_tld','statistical_report',
    'nb_hyperlinks','ratio_intHyperlinks','ratio_extHyperlinks','ratio_nullHyperlinks','nb_extCSS',
    'ratio_intRedirection','ratio_extRedirection','ratio_intErrors','ratio_extErrors','login_form','external_favicon',
    'links_in_tags','submit_email','ratio_intMedia','ratio_extMedia','sfh','iframe','popup_window','safe_anchor',
    'onmouseover','right_clic','empty_title','domain_in_title','domain_with_copyright','whois_registered_domain',
    'domain_registration_length','domain_age','web_traffic','dns_record','google_index','page_rank',
    'url_numeric_domain','url_numeric_path_length','url_numeric_num_subdomains','url_numeric_has_ip',
    'url_numeric_has_special_chars'
]

#convert the feature dictionary to a list to be safe 
feature_list = [feature_dictionary[feature] for feature in model_order]

#create the payload for the post request
data = {'features': feature_list}



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

except:
    print("Could not connect to the flask Server Make sure it is running and the features are correct")
