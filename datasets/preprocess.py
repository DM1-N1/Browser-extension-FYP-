import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder


# Load the dataset
original_dataset = pd.read_csv('datasets\dataset_phishing.csv')
dataset_no_url = pd.read_csv('datasets\dataset_no_url.csv')
dataset_with_url = pd.read_csv('datasets\dataset_with_url.csv')

# # STEP 1 
# # Drop non-URL-based features only if they exist in the dataset
# non_url_features = [

#     # Third-party dependent (excluded by your instruction)
#     'whois_registered_domain',
#     'domain_registration_length',
#     'domain_age',
#     'web_traffic',
#     'dns_record',
#     'google_index',
#     'page_rank',

#     'shortest_words_raw',               # Weak semantic signal
#     'path_extension',                   # Mostly 0 or noisy
#     'domain_in_title',                 # Often 0 or non-informative
#     'domain_with_copyright',           # Rare and inconsistent
#     'submit_email',                    # Almost always 0
#     'external_favicon',                # Unreliable signal
#     'login_form',                      # Often false negatives
#     'iframe',                          # Rare nowadays
#     'sfh'                              # Inconsistent across sites
# ]

# # Only drop columns that actually exist in the dataset
# columns_to_drop = [col for col in non_url_features if col in dataset_no_url.columns]
# print("Dropping columns:", columns_to_drop)

# dataset_no_url = dataset_no_url.drop(columns=columns_to_drop)
# dataset_with_url = dataset_with_url.drop(columns=columns_to_drop)

# # Save the updated dataset
# dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
# print("Cleaned dataset saved.")
# dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
# print("Cleaned dataset_no_url saved.")

#STEP 2
# dataset_no_url.drop(columns=['url'], inplace=True)
# dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
# print("Dropped URL column from dataset_no_url.")

# #STEP 3
# def extract_url_features(url):
#     parsed = urlparse(url)
#     return {
#         # Removed 'url_numeric_domain': parsed.netloc
#         'url_numeric_path_length': len(parsed.path),
#         'url_numeric_num_subdomains': parsed.netloc.count('.') - 1,
#         'url_numeric_has_ip': int(any(char.isdigit() for char in parsed.netloc)),
#         'url_numeric_has_special_chars': int(any(char in parsed.path for char in ['@', '-', '=']))
#     }

# # Extract features from URL column
# url_features = dataset_with_url['url'].apply(extract_url_features)
# url_features_df = pd.DataFrame(url_features.tolist())

# # Merge features back into dataset (excluding the 'url' column)
# dataset_with_url = pd.concat([dataset_with_url.drop(columns=['url']), url_features_df], axis=1)

# # Save the updated dataset
# dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
# print("URL features extracted and dataset_with_url updated.")

# #STEP 4
# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_no_url
dataset_no_url['status'] = dataset_no_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_no_url.to_csv('datasets\dataset_no_url.csv', index=False)
print("Mapped and saved dataset_no_url")

# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_with_url
dataset_with_url['status'] = dataset_with_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_with_url.to_csv('datasets\dataset_with_url.csv', index=False)
print("Mapped and saved dataset_with_url")

# ['length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens', 'nb_at',
#        'nb_qm', 'nb_and', 'nb_or', 'nb_eq', 'nb_underscore', 'nb_tilde',
#        'nb_percent', 'nb_slash', 'nb_star', 'nb_colon', 'nb_comma',
#        'nb_semicolumn', 'nb_dollar', 'nb_space', 'nb_www', 'nb_com',
#        'nb_dslash', 'http_in_path', 'https_token', 'ratio_digits_url',
#        'ratio_digits_host', 'punycode', 'port', 'tld_in_path',
#        'tld_in_subdomain', 'abnormal_subdomain', 'nb_subdomains',
#        'prefix_suffix', 'random_domain', 'shortening_service',
#        'nb_redirection', 'nb_external_redirection', 'length_words_raw',
#        'char_repeat', 'shortest_word_host', 'shortest_word_path',
#        'longest_words_raw', 'longest_word_host', 'longest_word_path',
#        'avg_words_raw', 'avg_word_host', 'avg_word_path', 'phish_hints',
#        'domain_in_brand', 'brand_in_subdomain', 'brand_in_path',
#        'suspecious_tld', 'statistical_report', 'nb_hyperlinks',
#        'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks',
#        'nb_extCSS', 'ratio_intRedirection', 'ratio_extRedirection',
#        'ratio_intErrors', 'ratio_extErrors', 'links_in_tags', 'ratio_intMedia',
#        'ratio_extMedia', 'popup_window', 'safe_anchor', 'onmouseover',
#        'right_clic', 'empty_title', 'url_numeric_path_length',
#        'url_numeric_num_subdomains', 'url_numeric_has_ip',
#        'url_numeric_has_special_chars']