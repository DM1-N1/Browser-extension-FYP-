#do 'pip install pandas if panda is not installed
# Importing the libraries
import pandas as pd
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder
import numpy as np
# Load the dataset 
# Make sure to use the correct path if othrs are running 
original_dataset = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_phishing.csv')
dataset_no_url = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_no_url.csv')
dataset_with_url = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_with_url.csv')


# Display the first few rows of the dataset
print(original_dataset.head())

#Check datatypes with all the rows showing 
print(original_dataset.dtypes)

# Ckecking if the datatset is balanced by checking legitamate against phishing in the status column
print(original_dataset['status'].value_counts())


dataset_no_url['status'] = dataset_no_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_no_url.to_csv('/workspaces/Browser-extension-FYP-/dataset_no_url.csv', index=False)

dataset_with_url['status'] = dataset_with_url['status'].map({'legitimate': 0, 'phishing': 1})
dataset_with_url.to_csv('/workspaces/Browser-extension-FYP-/dataset_with_url.csv', index=False)