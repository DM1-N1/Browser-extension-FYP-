import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense, Input  # type: ignore
from keras.optimizers import Adam  # type: ignore
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


dataset_with_url = pd.read_csv('datasets/dataset_with_url.csv')  # Ensure the path is correct
# x is the features only hence why we drop the target/classifier column 'status'
x = dataset_with_url.drop(columns=['status'])
# y is the target/classifier column 'status'
y = dataset_with_url['status']

# Split the dataset into training and testing sets. 80% for training and 20% for testing.
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, train_size=0.8, random_state=42, shuffle=True, stratify=y
)

# Scaling the features is important to ensure all the input variables are on a similar scale.
# This stops features with larger numerical values from dominating the training process 
# and improves the efficiency and accuracy of machine learning. 
# StandardScaler uses standardization, ensuring each feature has a mean of 0 and a standard deviation of 1.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the deep learning model
# Sequential model is used because it is good for simple layer-by-layer deep learning models
# It's good for tabular data and is a good comparison with traditional ML models.
model = Sequential()  # Sequential model allows you to stack layers one after another

# Input layer
model.add(Input(shape=(X_train_scaled.shape[1],)))

# Hidden layers with ReLU activation functions
model.add(Dense(128, activation='relu'))  # First hidden layer with 128 neurons
model.add(Dense(64, activation='relu'))   # Second hidden layer with 64 neurons

# Output layer with a sigmoid activation function for binary classification
model.add(Dense(1, activation='sigmoid'))  # Binary classifier

# Compile the model with Adam optimizer and binary cross-entropy loss for binary classification
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train the model
# epochs is the number of times the model will see the entire training data
history = model.fit(X_train_scaled, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Predict and evaluate on the test set
y_pred_probs = model.predict(X_test_scaled)
y_pred = (y_pred_probs > 0.5).astype("int32")  # Convert probabilities to binary predictions

# Show evaluation metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the scaler for later use in prediction
joblib.dump(scaler, "scaler.pkl")

# Save the trained deep learning model in .keras format (recommended format for TensorFlow models)
model.save("ai_model.keras")
