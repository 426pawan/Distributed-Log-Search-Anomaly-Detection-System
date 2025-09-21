import socket
import time
import os

SERVER_HOST = "127.0.0.1"  # Change to server IP if remote
SERVER_PORT = 5000
LOG_FILE = "/var/log/syslog"  # Change if needed

def follow(file):
    """Generator function that yields new lines in real time (like tail -f)."""
    file.seek(0, os.SEEK_END)  # Move to the end of file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)  # Wait for new data
            continue
        yield line

def send_logs():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Connected to server {SERVER_HOST}:{SERVER_PORT}")

        with open(LOG_FILE, "r") as f:
            loglines = follow(f)
            for line in loglines:
                client_socket.sendall(line.encode())
                print(f"[SENT] {line.strip()}")

if __name__ == "__main__":
    send_logs()
