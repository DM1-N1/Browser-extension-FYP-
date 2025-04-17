import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib


dataset_no_url = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_no_url.csv')
# x is the features only hecnce why we drop the target/classifier column status 
x = dataset_no_url.drop(columns=['status'])
# y is the target/classifier column status
y = dataset_no_url['status']

# Split the dataset into training and testing sets 20% of the data will be used for testing
# and 80% for training
# stratify=y ensures that the class distribution(0s & 1s or legit and phishing) is the same in both training and testing sets
# random_state=42 ensures that the split is reproducible
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, train_size=0.8, random_state=42, shuffle=True, stratify=y
)



#This part trains the RandomForest Classifier model
# n_estimators= is the number of decision trees the more trees the better the accuracy but it can slow down prediction time and training time
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# This part tests the model on the test set and prints the accuracy, confusion matrix, and classification report
# The accuracy score is the percentage of correct predictions
# The confusion matrix shows the number of true positives, true negatives, false positives, and false negatives
# The classification report shows the precision, recall, and f1-score for each class
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# joblib.dump(model, "random_forest_no_url.pkl")