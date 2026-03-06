from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from engine import process_image_to_csv, extract_total_price
from memory import store_in_memory
from database import init_db, add_item, get_all_items, clear_ledger

app = FastAPI()

init_db()

@app.get("/ledger")
def fetch_ledger():
    return {"items": get_all_items()}

@app.post("/ledger/add")
def post_item(name: str, price: float):
    add_item(name, price)
    return {"status": "success"}

@app.post("/ledger/clear")
def delete_ledger():
    clear_ledger()
    return {"status": "cleared"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 1. Extract text
    raw_text = process_image_to_csv(img)
    
    # 2. Extract money
    total_detected = extract_total_price(raw_text)
    
    # 3. Save to Vector DB
    store_in_memory(raw_text, {"filename": file.filename, "total": total_detected})
    
    # 4. Send back to Streamlit
    return {
        "filename": file.filename, 
        "csv": raw_text, 
        "detected_total": total_detected
    }