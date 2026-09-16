import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder


# Load the dataset
original_dataset = pd.read_csv('datasets\dataset_phishing.csv')
dataset_no_url = pd.read_csv('datasets\dataset_no_url.csv')
dataset_with_url = pd.read_csv('datasets\dataset_with_url.csv')

# STEP 1 
# Drop non-URL-based features only if they exist in the dataset
non_url_features = [

    # Third-party dependent (excluded by your instruction)
    'whois_registered_domain',
    'domain_registration_length',
    'domain_age',
    'web_traffic',
    'dns_record',
    'google_index',
    'page_rank',
     'nb_redirection',
   'nb_external_redirection',

    'shortest_words_raw',               # Weak semantic signal
    'path_extension',                   # Mostly 0 or noisy
    'domain_in_title',                 # Often 0 or non-informative
    'domain_with_copyright',           # Rare and inconsistent
    'submit_email',                    # Almost always 0
    'external_favicon',                # Unreliable signal
    'login_form',                      # Often false negatives
    'iframe',                          # Rare nowadays
    'sfh'                              # Inconsistent across sites
]

# Only drop columns that actually exist in the dataset
columns_to_drop = [col for col in non_url_features if col in dataset_no_url.columns]
print("Dropping columns:", columns_to_drop)

dataset_no_url = dataset_no_url.drop(columns=columns_to_drop)
dataset_with_url = dataset_with_url.drop(columns=columns_to_drop)

# Save the updated dataset
dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
print("Cleaned dataset saved.")
dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
print("Cleaned dataset_no_url saved.")

# STEP 2
dataset_no_url.drop(columns=['url'], inplace=True)
dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
print("Dropped URL column from dataset_no_url.")

#STEP 3
def extract_url_features(url):
    parsed = urlparse(url)
    return {
        # Removed 'url_numeric_domain': parsed.netloc
        'url_numeric_path_length': len(parsed.path),
        'url_numeric_num_subdomains': parsed.netloc.count('.') - 1,
        'url_numeric_has_ip': int(any(char.isdigit() for char in parsed.netloc)),
        'url_numeric_has_special_chars': int(any(char in parsed.path for char in ['@', '-', '=']))
    }

# Extract features from URL column
url_features = dataset_with_url['url'].apply(extract_url_features)
url_features_df = pd.DataFrame(url_features.tolist())

# Merge features back into dataset (excluding the 'url' column)
dataset_with_url = pd.concat([dataset_with_url.drop(columns=['url']), url_features_df], axis=1)

# Save the updated dataset
dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
print("URL features extracted and dataset_with_url updated.")

#STEP 4
# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_no_url
dataset_no_url['status'] = dataset_no_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_no_url.to_csv('datasets\dataset_no_url.csv', index=False)
print("Mapped and saved dataset_no_url")

# Map 'legitimate' to 0 and 'phishing' to 1 in dataset_with_url
dataset_with_url['status'] = dataset_with_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_with_url.to_csv('datasets\dataset_with_url.csv', index=False)
print("Mapped and saved dataset_with_url")

# STEP 5
# Drop 'ratio_extRedirection' from the already-preprocessed datasets.
# Removed because computing it live requires firing an HTTP request at every
# external link/script/css/media/favicon found on a page with no timeout,
# which was the main cause of slow classification in app.py. See notes.txt.
redirection_features = ['ratio_extRedirection']

columns_to_drop_step5 = [col for col in redirection_features if col in dataset_no_url.columns]
print("Dropping columns (step 5):", columns_to_drop_step5)

dataset_no_url = dataset_no_url.drop(columns=columns_to_drop_step5)
dataset_with_url = dataset_with_url.drop(columns=[col for col in redirection_features if col in dataset_with_url.columns])

dataset_no_url.to_csv('datasets/dataset_no_url.csv', index=False)
print("Dropped ratio_extRedirection and saved dataset_no_url.")
dataset_with_url.to_csv('datasets/dataset_with_url.csv', index=False)
print("Dropped ratio_extRedirection and saved dataset_with_url.")

