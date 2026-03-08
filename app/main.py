from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import logging
import numpy as np
import cv2
from typing import List, Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Local imports
from app.database import (
    init_db,
    add_item,
    get_all_items,
    delete_item_by_id,
    clear_database
)

from app.engine import process_image_to_text, llm_extract_items
from app.vector_store import add_to_vector_store, query_vector_store
from app.utils import clean_extracted_text

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("FastAPI Backend")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logger.info("Database initialized successfully on startup.")
    except Exception as e:
        logger.critical(f"Database init failed: {e}")

    yield
    logger.info("Server shutting down.")


app = FastAPI(lifespan=lifespan)


# Models
class Item(BaseModel):
    id: Optional[str] = None
    name: str
    price: float


class UpdateItem(BaseModel):
    id: str
    name: str
    price: float


class DeleteItems(BaseModel):
    item_ids: List[str]


# Routes
@app.get("/ledger")
async def fetch_ledger():
    try:
        items = get_all_items()
        return {"items": items}
    except Exception as e:
        logger.error(f"Error fetching ledger: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ledger.")

@app.put("/ledger/update")
async def update_item(item: UpdateItem):
    try:
        success = delete_item_by_id(item.id)

        if not success:
            raise HTTPException(status_code=404, detail="Item not found")

        add_item(item.id, item.name, item.price)

        logger.info(f"Updated item {item.id}")
        return {"status": "updated", "id": item.id}

    except Exception as e:
        logger.error(f"Update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item.")

# Delete multiple items
@app.delete("/ledger/delete/{item_id}")
async def delete_single_item(item_id: str):
    try:
        success = delete_item_by_id(item_id)

        if not success:
            raise HTTPException(status_code=404, detail="Item not found")

        logger.info(f"Deleted item {item_id}")
        return {"status": "deleted", "id": item_id}

    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete item.")


@app.delete("/ledger/delete")
async def delete_multiple_items(data: DeleteItems):
    try:
        deleted_count = 0

        for item_id in data.item_ids:
            if delete_item_by_id(item_id):
                deleted_count += 1

        logger.info(f"Deleted {deleted_count} items")
        return {"status": "deleted", "count": deleted_count}

    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete items.")


@app.delete("/ledger/clear")
async def clear_ledger():
    try:
        clear_database()
        logger.info("Ledger cleared")
        return {"status": "cleared"}
    except Exception as e:
        logger.error(f"Clear error: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear ledger.")


# Receipt Upload
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        raw_text = process_image_to_text(img)

        cleaned_text = clean_extracted_text(raw_text)

        suggested_items = llm_extract_items(cleaned_text)

        for item in suggested_items:
            item["id"] = str(uuid.uuid4())
            item["price"] = float(item.get("price", 0.0))

        return {
            "filename": file.filename,
            "suggested_items": suggested_items
        }

    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )