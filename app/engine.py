import pytesseract
import re
import os
import uuid
import cv2
import logging

# Configure logger
logger = logging.getLogger(__name__)

# 1. Environment-aware Tesseract path configuration
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


def preprocess_image(img):
    """
    Crops the OpenCV image (numpy array) to ignore phone UI elements.
    """
    height, width = img.shape[:2]

    # Crop top 15% and bottom 20% to remove phone UI bars
    start_y = int(height * 0.15)
    end_y = int(height * 0.80)

    return img[start_y:end_y, 0:width]


def process_image_to_text(img):
    """
    Performs OCR on an OpenCV image with improved preprocessing.
    """
    try:
        cleaned_img = preprocess_image(img)

        # Convert to grayscale
        gray = cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2GRAY)

        # Blur to remove noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive threshold (makes receipt text clearer)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        text = pytesseract.image_to_string(thresh)

        return text

    except Exception as e:
        logger.error(f"Error during OCR: {str(e)}")
        return ""


def llm_extract_items(text):
    """
    Parses OCR text into a list of dictionaries using robust regex.
    """
    items = []
    lines = text.split('\n')

    # Filter noise
    blacklist = ['ds', 'title', 'notes', 'shopping', 'list', 'q', 'o', 'we', 'total']

    # Regex pattern for item + price
    regex_pattern = r'([A-Za-z]{2,})\s*[:\-]?\s*[\$]?\s*(\d+(?:\.\d{1,2})?)'

    for line in lines:
        cleaned_line = line.strip()

        if cleaned_line:
            match = re.search(regex_pattern, cleaned_line, re.IGNORECASE)

            if match:
                name = match.group(1).strip()
                price_str = match.group(2)

                if len(name) > 1 and name.lower() not in blacklist:
                    try:
                        items.append({
                            "id": str(uuid.uuid4()),
                            "name": name,
                            "price": float(price_str)
                        })
                    except ValueError:
                        logger.warning(f"Failed to parse price for: {name}")

            else:
                logger.debug(f"Line ignored: {cleaned_line}")

    return items