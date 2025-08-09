import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load new dataset
df = pd.read_csv("multi_disease_dataset.csv")

# Features and target
X = df.drop(columns=["disease"])
y = df["disease"]

# Split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as disease_model.pkl")
print("Accuracy:", model.score(X_test, y_test))
