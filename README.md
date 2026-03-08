# 💰 AI Receipt Ledger

A full-stack application that processes receipt images using OCR, extracts item data via LLM, and manages a persistent inventory in a SQLite database.

## 🏗 System Architecture
The project is split into a modular backend and an interactive frontend:
- **Backend:** FastAPI (handles image processing, LLM logic, and database operations).
- **Frontend:** Streamlit (user dashboard for uploading, viewing, and deleting items).
- **Database:** SQLite (persistent storage for your ledger).



## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Install dependencies:
  `pip install fastapi uvicorn streamlit requests pandas opencv-python sqlalchemy`

### Running the App
1. **Launch the Backend:**
   Open a terminal in the project root:
   ```bash
   uvicorn app.main:app --reload
Launch the Frontend:
Open a second terminal in the project root:

streamlit run ui/dashboard.py
🛠 Troubleshooting Guide
"ModuleNotFoundError: No module named 'app...'"
If you encounter import errors, ensure you are running your commands from the root directory (where the app/ and ui/ folders live). Your project is structured as a Python package, so Python needs to be able to see the app/ folder as a module.

"404 Not Found" during deletion
This error typically indicates that the ID passed from the frontend does not match the record in the database.

Ensure your delete_item_by_id function in database.py is correctly executing the DELETE SQL command.

If the ledger becomes inconsistent, use the /ledger/clear endpoint to wipe the database and start fresh.

"Label got an empty value" (Streamlit Warning)
If you see terminal warnings regarding empty labels, check that all st.checkbox components have label_visibility="collapsed" and a non-empty string for the label.
