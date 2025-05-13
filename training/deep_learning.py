import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

dataset_with_url = pd.read_csv('datasets\dataset_with_url.csv')
# x is the features only hecnce why we drop the target/classifier column status 
x = dataset_with_url.drop(columns=['status'])
# y is the target/classifier column status
y = dataset_with_url['status']


X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, train_size=0.8, random_state=42, shuffle=True, stratify=y
)

# Scaling the features is important in order to ensure all the input variables are on a similar scale.
#This stops features with larger numerical values from dominating 
# the training process and improves the efficiency and accuracy of machine learning. 
# StandardScaler uses standardisation making sure each feature has a mean of 0 and a standard deviation of 1 for a 
# smoother and more reliable training process.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the model
# model.add is for the different layers of the model and what type of activation function is used  for each layer
# The activation function is a mathematical function that determines the output of a node in a neural network
model = Sequential()  # Sequential model was used because its good for simple layer by layer deep learning model
# Its good for tabular data like mine and is good for comparison with traditional ML models like the
# ones used in the train_model.py file
model.add(Input(shape=(X_train_scaled.shape[1],)))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classifier

# This part compiles the model
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# This part trains the model
#epochs is the number of times the model will see the entire training data
history = model.fit(X_train_scaled, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Predict and evaluate
y_pred_probs = model.predict(X_test_scaled)
y_pred = (y_pred_probs > 0.5).astype("int32")

# Show metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

#save the scaler
joblib.dump(scaler, "scaler.pkl")

#save the model
model.save("ai_model.h5")