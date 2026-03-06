import cv2
import pytesseract
import re

def process_image_to_csv(img):
    # Perform OCR
    text = pytesseract.image_to_string(img)
    return text

def extract_total_price(text):
    # Looks for numbers like 10.99 or 500.00
    prices = re.findall(r'\d+\.\d{2}', text)
    if not prices:
        return 0.0
    # Convert strings to floats and pick the max (usually the total)
    float_prices = [float(p) for p in prices]
    return max(float_prices)