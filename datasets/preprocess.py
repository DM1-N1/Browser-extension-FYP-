import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder


# Load the dataset
original_dataset = pd.read_csv('datasets\dataset_phishing.csv')
dataset_no_url = pd.read_csv('datasets\dataset_no_url.csv')
dataset_with_url = pd.read_csv('datasets\dataset_with_url.csv')

#STEP 1 
# Drop non-URL-based features only if they exist in the dataset
# non_url_features = [
#     'ip', 'nb_hyperlinks', 'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks', 
#     'nb_extCSS', 'ratio_intRedirection', 'ratio_extRedirection', 'ratio_intErrors', 'ratio_extErrors',
#     'login_form', 'external_favicon', 'links_in_tags', 'submit_email', 'ratio_intMedia', 'ratio_extMedia',
#     'sfh', 'iframe', 'popup_window', 'safe_anchor', 'onmouseover', 'right_clic', 'empty_title', 
#     'domain_with_copyright', 'google_index', 'page_rank', 'domain_in_brand', 'brand_in_subdomain',
#     'brand_in_path', 'suspecious_tld', 'statistical_report'
# ]

# # Only drop columns that actually exist in the dataset
# columns_to_drop = [col for col in non_url_features if col in dataset_no_url.columns]
# print("Dropping columns:", columns_to_drop)

# dataset_with = dataset_with_url.drop(columns=columns_to_drop)

# # Save the updated dataset
# dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
# print("Cleaned dataset saved.")

#STEP 2
# dataset_no_url.drop(columns=['url'], inplace=True)
# dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
# print("Dropped URL column from dataset_no_url.")

#STEP 3
# def extract_url_features(url):
#     parsed = urlparse(url)
#     return {
#         'url_numeric_domain': parsed.netloc,
#         'url_numeric_path_length': len(parsed.path),
#         'url_numeric_num_subdomains': parsed.netloc.count('.') - 1,
#         'url_numeric_has_ip': int(any(char.isdigit() for char in parsed.netloc)),
#         'url_numeric_has_special_chars': int(any(char in parsed.path for char in ['@', '-', '=']))
#     }

# # Extract features from URL column
# url_features = dataset_with_url['url'].apply(extract_url_features)
# url_features_df = pd.DataFrame(url_features.tolist())

# # Convert domain to numerical values
# url_features_df['url_numeric_domain'] = LabelEncoder().fit_transform(url_features_df['url_numeric_domain'])

# # Merge features back into dataset
# dataset_with_url = pd.concat([dataset_with_url.drop(columns=['url']), url_features_df], axis=1)

# # Save the updated dataset
# dataset_with_url.to_csv('datasets\dataset_with_url.csv', index=False)
# print("URL features extracted and dataset_with_url updated.")

#STEP 4
# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_no_url
dataset_no_url['status'] = dataset_no_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_no_url.to_csv('datasets\dataset_no_url.csv', index=False)
print("Mapped and saved dataset_no_url")

# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_with_url
dataset_with_url['status'] = dataset_with_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_with_url.to_csv('datasets\dataset_with_url.csv', index=False)
print("Mapped and saved dataset_with_url")