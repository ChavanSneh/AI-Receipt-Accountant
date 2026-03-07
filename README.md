🛒 AI Receipt Accountant
An automated expense tracker that uses OCR (Optical Character Recognition) to read receipts and an SQLite database inside a Docker container to keep a persistent ledger of your shopping.
🚀 Features
 * AI Receipt Scanning: Upload images (JPG/PNG) of receipts to extract item names and prices.
 * Persistent Ledger: Data is saved to a local SQLite database (ledger.db) inside Docker, so it survives app restarts.
 * Real-time UI: Built with Streamlit for a smooth, interactive experience.
 * Data Export: Download your entire shopping history as a CSV file.
🛠️ Tech Stack
 * Frontend: Streamlit
 * Backend: FastAPI
 * Database: SQLite
 * Containerization: Docker
 * OCR: Python-tesseract / Google Vision (depending on your main.py setup)
📦 How to Run
1. Start the Backend (The Brain)
Build and run the Docker container to handle the OCR and Database:
# Build the image
docker build -t receipt-api .

# Run the container (Mapping port 8000)
docker run -p 8000:8000 receipt-api

2. Start the Frontend (The Face)
Open a new terminal and run the Streamlit app:
# Install requirements locally
pip install -r requirements.txt

# Launch the app
streamlit run app.py

📂 Project Structure
 * app.py: Streamlit UI logic.
 * main.py: FastAPI endpoints for processing images and managing the database.
 * database.py: Logic for creating tables and saving/fetching ledger data.
 * Dockerfile: Instructions to containerize the backend.
 * requirements.txt: Python dependencies.
📝 Future Improvements
 * [ ] Add Category classification (Food, Electronics, etc.).
 * [ ] Support for multi-page PDF receipts.
 * [ ] Monthly spending charts using Plotly.
