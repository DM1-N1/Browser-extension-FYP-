# I have chosen to keep this file in order to show the steps I took to preprocess the dataset
# The code is not run and is not needed for the final code to run

#do 'pip install pandas if panda is not installed
# Importing the libraries
import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder
import numpy as np
# Load the dataset 
# Make sure to use the correct path if othrs are running 
original_dataset = pd.read_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_phishing.csv')
dataset_no_url = pd.read_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_no_url.csv')
dataset_with_url = pd.read_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_with_url.csv')


# # STEP 1 
# # Display the first few rows of the dataset
# print(original_dataset.head())

# #Check datatypes with all the rows showing 
# print(original_dataset.dtypes)

# # Ckecking if the datatset is balanced by checking legitamate against phishing in the status column
# print(original_dataset['status'].value_counts())

# # Drops the url column from the datset and create a copy 

# try:
#     original_dataset.drop(columns=['url'], inplace=True) 
#     print("Url column dropped")
#     original_dataset.to_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_no_url_.csv', index=False)
#     print("Updated dataset saved to 'dataset_no_url.csv'")
# except:
#     print("Column has already been dropped")


# # Get features from the url to change to numerical values
# def extract_url_features(url):
#     parsed = urlparse(url)
#     return {
#         'url_numeric_domain': parsed.netloc,
#         'url_numeric_path_length': len(parsed.path),
#         'url_numeric_num_subdomains': parsed.netloc.count('.') - 1,
#         'url_numeric_has_ip': int(any(char.isdigit() for char in parsed.netloc)),
#         'url_numeric_uses_https': int(parsed.scheme == 'https'),
#         'url_numeric_has_special_chars': int(any(char in parsed.path for char in ['@', '-', '=']))
#     }

# # apply feature extraction
# features = original_dataset['url'].apply(extract_url_features)
# features_df = pd.DataFrame(features.tolist())

# # Make the url_numeric_domain' a numerical value 
# features_df['url_numeric_domain'] = LabelEncoder().fit_transform(features_df['url_numeric_domain'])
# dataset = pd.concat([original_dataset.drop(columns=['url']), features_df], axis=1)
# print("Url converted to numerical")
# dataset.to_csv("dataset_with_url.csv", index=False)


# # Map the features for comparison
# feature_checks = {
#     'url_numeric_has_ip': ['ip'],
#     'url_numeric_uses_https': ['https_token'],
#     'url_numeric_path_length': ['length_url'],
#     'url_numeric_num_subdomains': ['nb_subdomains'],
#     'url_numeric_has_special_chars': ['nb_at', 'nb_hyphens', 'nb_eq'],
# }

# # Compare numeric features with the original dataset
# for extracted_feat, matches in feature_checks.items():
#     if extracted_feat == 'url_numeric_domain':
#         continue 

#     for match in matches:
#         if extracted_feat in dataset.columns and match in dataset.columns:
#             print(f"\nComparing: {extracted_feat} and {match}")
            
#             if (dataset[extracted_feat] == dataset[match]).all():
#                 print(" Identical values — consider dropping one.")
#                 continue

#             corr = np.corrcoef(dataset[extracted_feat], dataset[match])[0, 1]
#             print(f" Correlation: {corr:.4f}")

#             if abs(corr) > 0.95:
#                 print(" High correlation probably a duplicate.")
#             elif abs(corr) > 0.5:
#                 print(" Medium correlation might be useful ")
#             else:
#                 print(" Low correlation most likely keep this.")
#         else:
#             print(f" Skipping: '{extracted_feat}' or '{match}' not found.")

# #Drop columns based on comparison            

# columns_to_drop = ['url_numeric_uses_https']
# original_dataset.drop(columns=columns_to_drop, inplace=True)
# print("Column dropped")
# # # Save the cleaned dataset
# original_dataset.to_csv("updated.csv", index=False)
# print("Dataset saved")

# # STEP 3
# dataset_no_url['status'] = dataset_no_url['status'].map({'legitimate': 0, 'phishing': 1})
# dataset_no_url.to_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_no_url.csv', index=False)

# dataset_with_url['status'] = dataset_with_url['status'].map({'legitimate': 0, 'phishing': 1})
# dataset_with_url.to_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_with_url.csv', index=False)

# List of columns to drop
columns_to_remove = [
    'nb_dslash', 'https_token', 'nb_subdomains', 'length_words_raw', 
    'char_repeat', 'shortest_word_host', 'avg_words_raw', 'avg_word_host', 
    'domain_in_title', 'dns_record', 'whois_registered_domain', 
    'domain_registration_length', 'domain_age', 'web_traffic'
]

columns_to_remove_with_url = [col for col in columns_to_remove if col in dataset_with_url.columns]
dataset_with_url.drop(columns=columns_to_remove_with_url, inplace=True)
dataset_with_url.to_csv('N:\Browser-extension-FYP- - Copy\datasets\dataset_with_url.csv', index=False)
print(f"Updated dataset_with_url saved to 'N:\\Browser-extension-FYP- - Copy\\datasets\\dataset_with_url.csv'. Columns removed: {columns_to_remove_with_url}")