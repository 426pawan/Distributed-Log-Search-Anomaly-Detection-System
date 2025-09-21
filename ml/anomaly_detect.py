import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
import joblib

# Load parsed logs
logs = pd.read_csv("parsed_logs.csv")

# Use only the "message" column for now
vectorizer = TfidfVectorizer(max_features=500)
X = vectorizer.fit_transform(logs["message"])

# Train Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)

# Save model + vectorizer
joblib.dump(model, "models/isolation_forest.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Isolation Forest model trained & saved.")
