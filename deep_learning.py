import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

dataset_no_url = pd.read_csv('/workspaces/Browser-extension-FYP-/dataset_no_url.csv')
# x is the features only hecnce why we drop the target/classifier column status 
x = dataset_no_url.drop(columns=['status'])
# y is the target/classifier column status
y = dataset_no_url['status']

# Scale the features (important for deep learning)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, train_size=0.8, random_state=42, shuffle=True, stratify=y
)

# Build the model
model = Sequential()
model.add(Input(shape=(X_train.shape[1],)))
model.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

# Compile the model
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Predict and evaluate
y_pred_probs = model.predict(X_test)
y_pred = (y_pred_probs > 0.5).astype("int32")

# Show metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
