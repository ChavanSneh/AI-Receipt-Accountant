import re

def clean_extracted_text(text):
    """Basic helper to remove junk characters from OCR output."""
    # Example: remove unwanted symbols or whitespace
    clean_text = re.sub(r'[^\w\s.$]', '', text)
    return clean_text.strip()

def calculate_analytics(items):
    """Processes a list of items to return spending insights."""
    if not items:
        return {"total": 0, "count": 0}
    
    total = sum(item['price'] for item in items)
    return {
        "total_spent": round(total, 2),
        "total_items": len(items)
    }