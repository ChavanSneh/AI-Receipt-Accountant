# 🛒 AI Receipt Accountant (2026 Edition)

An automated financial pipeline that turns receipt images into a searchable digital ledger. This isn't just a script; it's a **containerized AI system**.

## 🚀 Key Features
* **AI Vision:** Extracts item names and prices from JPG/PNG uploads.
* **Smart Memory:** Uses **ChromaDB** for vector-based search (Search for "snacks" and find the "Chips" receipt).
* **Dockerized:** Runs in a consistent environment using a single Docker image.
* **Export Ready:** Download your entire history as a CSV for Excel.

## 🏗️ The System Architecture
This project is built using a **Modular Design** (Decoupled Architecture):
* **`app_ui.py`**: The "Face" (Frontend) built with Streamlit.
* **`engine.py`**: The "Brain" (Logic) that processes the OCR.
* **`memory.py`**: The "Memory" (Vector DB) using ChromaDB.
* **`database.py`**: The "Storage" (SQL) for the permanent ledger.

## 🛠️ Tech Stack
* **Language:** Python 3.10-slim
* **Framework:** FastAPI & Streamlit
* **AI/OCR:** Tesseract & ChromaDB (Vector Store)
* **Infrastructure:** Docker

## 📦 Quick Start (The Orchestrator Move)
1. **Build the Box:** `docker build -t receipt-api .`
2. **Launch the API:** `docker run -p 8000:8000 receipt-api`
3. **Run the UI:** `streamlit run app_ui.py`
