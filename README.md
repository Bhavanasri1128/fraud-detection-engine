# Multi-Bank Credit Card Fraud Detection Engine (Python & SQLite)

A modular fraud detection and alert investigation engine built with **Python** and **SQLite**, featuring real-time risk scoring and SHA-256 inter-bank threat sharing.

## Key Features
- **Real-Time Risk Scoring**: Evaluates credit limit utilization and cross-bank threat intelligence to assign a 0–100 risk score (`Approve`, `Verify`, or `Decline`).
- **Privacy-Preserving Threat Sharing (`SHA-256`)**: Hashes compromised device IDs before storing them in the consortium `SHARED_THREATS` table so participating banks detect repeat attackers immediately.
- **Persistent SQLite Storage**: Tracks multi-bank cards (`CARDS`), fraud alerts (`ALERTS`), and shared indicators (`SHARED_THREATS`).

## Project Structure
- `database.py` — Initializes the normalized SQLite schema and seed card data
- `engine.py` — Core risk scoring, SHA-256 device hashing, and alert resolution logic
- `main.py` — Menu-driven CLI console for scoring transactions and resolving alerts
- `test_fraud.py` — Automated unit tests using Python's `unittest` framework

## How to Run
1. Clone or download this repository.
2. Run `python main.py` (or open `main.py` in IDLE and press `F5`).
3. Run unit tests using `python -m unittest test_fraud.py`.
