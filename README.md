# Distributed Log Search & Anomaly Detection System

A modular, distributed system to collect logs from multiple Linux servers, store them in a searchable index, and detect anomalies using machine learning.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Phases](#phases)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Machine Learning](#machine-learning)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

This system collects logs from multiple Linux nodes, centralizes them in a server, makes them searchable, and detects anomalous events using an Isolation Forest model. It is modular and can be extended for distributed deployment and visualization.

---

## Features

- TCP/IP-based log collection from multiple Linux servers
- Centralized storage with Whoosh search index
- Real-time anomaly detection using Isolation Forest
- Multi-threaded server to handle concurrent clients
- Option to visualize anomalies via a dashboard (Phase 4)
- Logs and anomalies stored separately for auditing

---

## Phases

### Phase 1: TCP/IP Log Collector

- Client agent runs on Linux servers
- Collects `/var/log/syslog` or `/var/log/auth.log`
- Sends logs to central server using TCP sockets

### Phase 2: Central Log Storage & Search

- Stores logs in Whoosh index for fast search
- CLI tool `search.py` for keyword, host, or time queries
- Supports multiple concurrent connections

### Phase 3: Machine Learning for Anomaly Detection

- Preprocess logs (timestamp, host, process, message)
- Train Isolation Forest to detect unusual patterns
- Detects anomalies like:
  - Multiple failed logins
  - Repeated connection attempts (DDoS-like)
- Anomalies saved to `anomalies.log`

### Phase 4: Distributed Deployment & Visualization (Optional)

- Deploy agents + server using Docker/Kubernetes
- Build web dashboard using Flask/FastAPI + React
- REST API for querying logs and anomalies

---

### Project Structure

distributed-log-analyzer/
│
├── agent/                   # Client agent (Linux)
│   ├── agent.py             # Collects logs and sends via TCP
│   └── config.yaml          # Agent config (server IP, port, log path)
│
├── server/                  # Central server
│   ├── server.py            # Multi-threaded TCP server with anomaly detection
│   ├── storage.py           # Stores logs in Whoosh index
│   ├── search.py            # CLI search tool
│   ├── logs.txt             # All collected logs
│   ├── anomalies.log        # Detected anomalies
│   └── indexdir/            # Whoosh index files
│
├── ml/                      # Machine learning
│   ├── preprocess.py        # Parse logs into structured CSV
│   ├── anomaly_detect.py    # Train Isolation Forest model
│   ├── detect_realtime.py   # Test real-time anomaly detection
│   └── models/              # Saved model & vectorizer
│
├── scripts/                 # Utility scripts
│   ├── run_agent.sh
│   └── run_server.sh
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


---

### Prerequisites

-   **OS:** Linux (Ubuntu/Debian recommended)
-   **Python:** 3.9+
-   **Git:** for version control
-   **Docker/Kubernetes:** optional (for Phase 4)
-   **Python libraries:** `pandas`, `scikit-learn`, `joblib`, `Whoosh`, `Flask` or `FastAPI`, `threading` (built-in)

---

### Setup & Installation

```bash
# Clone repository
git clone <repository_url>
cd distributed-log-analyzer

# Install Python dependencies
pip install -r requirements.txt
Usage
1️⃣ Start Server

Bash

cd server
python3 server.py
2️⃣ Start Agent (Send Logs)

Bash

cd agent
sudo python3 agent.py
3️⃣ Run Search

Bash

cd server
python3 search.py
# Enter a keyword to see matching logs
4️⃣ Preprocess Logs for ML

Bash

cd ml
python3 preprocess.py
5️⃣ Train Isolation Forest Model

Bash

python3 anomaly_detect.py
6️⃣ Real-time Anomaly Detection

Server will automatically detect anomalies as logs arrive.

All logs are saved in server/logs.txt.

Anomalies are saved in server/anomalies.log.

Whoosh index keeps logs searchable.

Machine Learning
Model: Isolation Forest (unsupervised anomaly detection)

Input Features: TF-IDF vectorized log messages

Output: -1 = anomaly, 1 = normal

Model saved in: ml/models/isolation_forest.pkl

Vectorizer saved in: ml/models/vectorizer.pkl

Future Improvements
Deploy agents + server using Docker/Kubernetes for distributed scaling.

Add a web dashboard to visualize anomalies in real-time.

Switch to Elasticsearch for handling large-scale logs.

Integrate secure TLS sockets for log transfer.

Experiment with LSTM Autoencoder for sequential anomaly detection.

License
This project is licensed under the MIT License.

## Project Structure

