import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pickle
import sklearn

# Define proper column names based on your API (6 features + class)
column_names = ['temp', 'maxt', 'wspd', 'cloudcover', 'percip', 'humidity', 'class']

# Load both datasets
data0 = pd.read_csv("data1.csv", names=column_names)  # Class 0 (No Flood)
data1 = pd.read_csv("data.csv", names=column_names)   # Class 1 (Flood)

# Merge both datasets
data = pd.concat([data0, data1], ignore_index=True)

# Display dataset info
print("Available columns:", data.columns)
print("Dataset preview:\n", data.head())
print("Missing values:\n", data.isnull().sum())

# Ensure 'class' column exists
if 'class' not in data.columns:
    raise KeyError("The 'class' column is missing. Check the CSV file formatting.")

# Handle missing values in 'class'
if data['class'].isnull().sum() > 0:
    print("⚠️ Warning: 'class' column has missing values. Filling with random 0 or 1 for testing.")
    data['class'].fillna(np.random.choice([0, 1]), inplace=True)  # TEMPORARY FIX

# Convert 'class' column to integer
data['class'] = data['class'].astype(int)

# Check for label balance
print("Class distribution:\n", data['class'].value_counts())

# Handle any remaining missing values in features
data.dropna(inplace=True)  # Drop rows where any feature has NaN

# Splitting features and target
y = data['class']
X = data.drop('class', axis=1)

# Ensure dataset is not empty after preprocessing
if X.empty or y.empty:
    raise ValueError("Dataset is empty after preprocessing. Check CSV file.")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Model
classifier = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)
classifier.fit(X_train, y_train)

# Predictions & Accuracy
pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("Accuracy: {:.2f}%".format(accuracy * 100))

# Save the trained model with scikit-learn version metadata
model_data = {
    "model": classifier,
    "sklearn_version": sklearn.__version__
}

pickle.dump(model_data, open('model.pickle', 'wb'))
print("✅ Model saved successfully as 'model.pickle'")

# API Data Fetching Function
def get_data(latitude, longitude):
    response = your_api_call_here()  # Replace with actual API call
    if 'items' in response and len(response['items']) > 0:
        lat = response['items'][0]['position']['lat']
        lon = response['items'][0]['position']['lng']
        return fetch_weather_data(lat, lon)
    else:
        raise ValueError("Invalid API response: 'items' not found")
