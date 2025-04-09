#do 'pip install pandas if panda is not installed
# Importing the libraries
import pandas as pd
# Load the dataset 
# Make sure to use the correct path if othrs are running 
dataset = pd.read_csv('C:/Users/user/OneDrive/Desktop/Software engineering/Third year L6/Browser-extension-FYP-/dataset_phishing.csv')
print(dataset.head())

#Check datatypes
print(dataset.dtypes)