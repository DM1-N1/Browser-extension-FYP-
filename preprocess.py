#do 'pip install pandas if panda is not installed
# Importing the libraries
import pandas as pd
# Load the dataset 
# Make sure to use the correct path if othrs are running 
# dataset = pd.read_csv('C:/Users/user/OneDrive/Desktop/Software engineering/Third year L6/Browser-extension-FYP-/dataset_phishing.csv')
dataset = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_phishing.csv')
print(dataset.head())

#Check datatypes with all the rows showing 
pd.set_option('display.max_rows', None)
print(dataset.dtypes)

# Ckecking if the datatset is balanced by checking legitamate against phishing in the status column
print(dataset['status'].value_counts())

# Drops the url column from the datset and create a copy 

try:
    dataset.drop(columns=['url'], inplace=True) 
    print("Url column dropped")
    dataset.to_csv('/workspaces/Browser-extension-FYP-/dataset_phishing_no_url_updated.csv', index=False)
    print("Updated dataset saved to 'dataset_phishing_no_url_updated.csv'")
except:
    print("Column has already been dropped")
