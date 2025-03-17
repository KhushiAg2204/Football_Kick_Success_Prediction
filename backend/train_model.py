import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle  # To save the scaler

# Load dataset
# Load dataset
data = pd.read_csv('../football_data.csv', encoding='utf-8-sig')

# Remove spaces and standardize column names
data.columns = data.columns.str.strip().str.replace(" ", "_")

# Print cleaned column names (debugging)
print("Columns after cleaning:", data.columns)

# Replace NaN values with 0
data.fillna(0, inplace=True)

# Define features and target
X = data[['Speed', 'Angle', 'Distance', 'Goalkeeper_Position']]
y = data['Kick_Success']


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the scaler
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Build the neural network model
model = Sequential([
    Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01), input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    Dropout(0.2),
    Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Save the trained model
model.save('football_model.h5')

print("✅ Model training completed! `football_model.h5` and `scaler.pkl` saved.")


