import sqlite3
from engine import run_ocr, llm_extract_items # Adjust 'engine' if the name is different

def init_db():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def add_item(name, price):
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def get_all_items():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "price": row[1]} for row in rows]

def clear_ledger():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()

def update_item(item_id, new_name, new_price):
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    # SQL command to update specific columns for a specific ID
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (new_name, new_price, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def process_receipt_automatically(image_path):
    try:
        # 1. Get raw text from OCR
        raw_text = run_ocr(image_path)
        if not raw_text:
            print("Error: No text found in receipt.")
            return

        # 2. Extract items using LLM
        # Ensure your llm_extract_items returns a list of dicts, e.g., [{'name': 'Milk', 'price': 40.0}]
        items_found = llm_extract_items(raw_text) 
        
        if not isinstance(items_found, list):
            print("Error: LLM output is not in the expected list format.")
            return

        # 3. Auto-save to Database with validation
        for item in items_found:
            # Error Check: Ensure keys exist before adding
            name = item.get('name')
            price = item.get('price')
            
            if name and price is not None:
                # Convert price to float to avoid database errors
                add_item(str(name), float(price))
            else:
                print(f"Skipping incomplete item: {item}")
        
        print("Auto-added items to ledger successfully!")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")