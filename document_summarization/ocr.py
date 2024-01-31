from PIL import Image
import pytesseract

def perform_ocr(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

