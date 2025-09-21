import joblib

model = joblib.load("models/isolation_forest.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def detect_anomaly(log_message):
    X_new = vectorizer.transform([log_message])
    prediction = model.predict(X_new)  # -1 = anomaly, 1 = normal
    return "ANOMALY" if prediction[0] == -1 else "NORMAL"

# Example usage
sample = "Failed password for root from 192.168.1.10 port 22 ssh2"
print(sample, "→", detect_anomaly(sample))
