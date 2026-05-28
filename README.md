# 💰 AI Receipt Accountant

An intelligent, full-stack expense parsing engine that automates receipt digitisation. The system ingests receipt images using OCR, orchestrates structural data extraction via an LLM, and manages a persistent financial inventory.

---

## 🏗️ System Architecture

The project features a highly decoupled, modular architecture designed for high-throughput data processing:

*   **Backend (FastAPI):** Orchestrates image processing pipelines, handles LLM reasoning layers, and manages database operations.
  
*   **Frontend (Streamlit):** An interactive user dashboard for real-time receipt uploading, structured accountant viewing, and row-level record deletion.
  
*   **Database (SQLite):** Persistent relational storage layer for consistent accountant management.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.11+
*   Install core dependencies:
       pip install fastapi uvicorn streamlit requests pandas opencv-python sqlalchemy

### Running the App

1.  **Launch the Backend Service**
    uvicorn app.main:app --reload
    ```
2.  **Launch the Frontend Dashboard**

    streamlit run ui/dashboard.py
    ```

---

## 🛠️ Troubleshooting Guide

> 💡 **Tip:** Always execute commands directly from the root directory to maintain correct package paths.

| Issue | Root Cause | Resolution |
| :--- | :--- | :--- |
| **`ModuleNotFoundError: No module named 'app...'`** | Commands executed outside root directory; Python cannot see `app/` as a package. | Ensure your terminal is in the project root before running servers. |
| **`404 Not Found` during deletion** | Frontend ID mismatch with the active database record. | Verify `delete_item_by_id` in `database.py` is executing the `DELETE` SQL command correctly. |
| **Accountant state inconsistency** | Corrupted or out-of-sync local database rows. | Hit the `/ledger/clear` endpoint to safely wipe the database and start fresh. |
| **`Label got an empty value`** | Streamlit warning regarding hidden checkbox UI elements. | Ensure all `st.checkbox` components have `label_visibility="collapsed"` and a non-empty string label. |
