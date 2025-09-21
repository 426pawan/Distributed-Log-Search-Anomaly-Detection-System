import socket
import threading
import joblib
from storage import index_log

HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 5000        # Listening port

# Load trained anomaly detection model + vectorizer
try:
    model = joblib.load("../ml/models/isolation_forest.pkl")
    vectorizer = joblib.load("../ml/models/vectorizer.pkl")
    print("[+] Anomaly detection model loaded.")
except Exception as e:
    print(f"[!] Could not load anomaly detection model: {e}")
    model, vectorizer = None, None

LOG_FILE = "logs.txt"
ANOMALY_FILE = "anomalies.log"

def detect_anomaly(log_message: str) -> bool:
    """Return True if log is anomaly, else False"""
    if model is None or vectorizer is None:
        return False  # Fallback: no detection
    X_new = vectorizer.transform([log_message])
    prediction = model.predict(X_new)  # -1 = anomaly, 1 = normal
    return prediction[0] == -1

def save_log(log_line: str, file_path: str):
    """Append a log line to a file"""
    with open(file_path, "a") as f:
        f.write(log_line + "\n")

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            log_line = data.decode().strip()

            # Store in Whoosh index
            index_log(log_line)

            # Save all logs
            save_log(log_line, LOG_FILE)

            # Detect anomaly
            if detect_anomaly(log_line):
                print(f"[ANOMALY] {log_line}")
                save_log(log_line, ANOMALY_FILE)
            else:
                print(f"[LOG] {log_line}")

    print(f"[-] Connection closed: {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[+] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()