#do 'pip install pandas if panda is not installed
# Importing the libraries
import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder
import numpy as np
# Load the dataset 
# Make sure to use the correct path if othrs are running 
# dataset = pd.read_csv('C:/Users/user/OneDrive/Desktop/Software engineering/Third year L6/Browser-extension-FYP-/dataset_phishing.csv')
dataset = pd.read_csv('/workspaces/Browser-extension-FYP-/updated.csv')
# print(dataset.head())

# #Check datatypes with all the rows showing 
# pd.set_option('display.max_rows', None)
# print(dataset.dtypes)

# # Ckecking if the datatset is balanced by checking legitamate against phishing in the status column
# print(dataset['status'].value_counts())



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
# features = dataset['url'].apply(extract_url_features)
# features_df = pd.DataFrame(features.tolist())

# # Make the url_numeric_domain' a numerical value 
# features_df['url_numeric_domain'] = LabelEncoder().fit_transform(features_df['url_numeric_domain'])
# dataset = pd.concat([dataset.drop(columns=['url']), features_df], axis=1)
# print("Url converted to numerical")
# dataset.to_csv("updated.csv", index=False)


# Map of features for comparison
feature_checks = {
    'url_numeric_has_ip': ['ip'],
    'url_numeric_uses_https': ['https_token'],
    'url_numeric_path_length': ['length_url'],
    'url_numeric_num_subdomains': ['nb_subdomains'],
    'url_numeric_has_special_chars': ['nb_at', 'nb_hyphens', 'nb_eq'],
}

# Compare numeric features
for extracted_feat, matches in feature_checks.items():
    if extracted_feat == 'url_numeric_domain':
        continue 

    for match in matches:
        if extracted_feat in dataset.columns and match in dataset.columns:
            print(f"\nComparing: {extracted_feat} and {match}")
            
            if (dataset[extracted_feat] == dataset[match]).all():
                print(" Identical values — consider dropping one.")
                continue

            corr = np.corrcoef(dataset[extracted_feat], dataset[match])[0, 1]
            print(f" Correlation: {corr:.4f}")

            if abs(corr) > 0.95:
                print(" High correlation probably a duplicate.")
            elif abs(corr) > 0.5:
                print(" Medium correlation might be useful ")
            else:
                print(" Low correlation most likely keep this.")
        else:
            print(f" Skipping: '{extracted_feat}' or '{match}' not found.")