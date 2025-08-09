import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv('multi_disease_dataset.csv')

# Split features and labels
X = df.drop('disease', axis=1)
y = df['disease']

# Split into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")

# Save symptom list (column names) for reference
with open('symptoms_list.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)
