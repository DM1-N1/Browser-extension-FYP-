import pickle
import numpy as np

# Feature names as a list (split your string)
feature_names = [
    'length_url','length_hostname','ip','nb_dots','nb_hyphens','nb_at','nb_qm','nb_and','nb_or','nb_eq',
    'nb_underscore','nb_tilde','nb_percent','nb_slash','nb_star','nb_colon','nb_comma','nb_semicolumn',
    'nb_dollar','nb_space','nb_www','nb_com','nb_dslash','http_in_path','https_token','ratio_digits_url',
    'ratio_digits_host','punycode','port','tld_in_path','tld_in_subdomain','abnormal_subdomain','nb_subdomains',
    'prefix_suffix','random_domain','shortening_service','length_words_raw','char_repeat','shortest_word_host',
    'shortest_word_path','longest_words_raw','longest_word_host','longest_word_path','avg_words_raw','avg_word_host',
    'avg_word_path','phish_hints','domain_in_brand','brand_in_subdomain','brand_in_path','suspecious_tld',
    'statistical_report','nb_hyperlinks','ratio_intHyperlinks','ratio_extHyperlinks','ratio_nullHyperlinks',
    'nb_extCSS','ratio_intRedirection','ratio_extRedirection','ratio_intErrors','ratio_extErrors','links_in_tags',
    'ratio_intMedia','ratio_extMedia','popup_window','safe_anchor','onmouseover','right_clic','empty_title',
    'status','url_numeric_path_length','url_numeric_num_subdomains','url_numeric_has_ip','url_numeric_has_special_chars'
]

# Load the model
import joblib
model = joblib.load('ai_model.pkl')


# Extract feature importance or coefficients
if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
elif hasattr(model, 'coef_'):
    # If multiple classes, take the absolute mean of coefficients across classes
    coef = model.coef_
    if len(coef.shape) > 1:
        importances = np.mean(np.abs(coef), axis=0)
    else:
        importances = np.abs(coef)
else:
    raise ValueError("Model has no feature_importances_ or coef_ attribute")

# Pair features with importance and sort descending
feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

# Print the sorted features with their importance
print("Feature importances (sorted):")
for feat, imp in feat_imp:
    print(f"{feat}: {imp:.6f}")
