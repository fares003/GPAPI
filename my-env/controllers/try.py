import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os

# Set paths for Tesseract OCR and Poppler
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\MOHAMED\Downloads\poppler-24.08.0\Library\bin"

def preprocess_image(image):
    """Preprocess image for better OCR accuracy."""
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 31, 2)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return Image.fromarray(gray)

def extract_text_from_image(image):
    """Extract text from an image using Tesseract OCR."""
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(processed_image, lang='eng')
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF, using OCR for images if necessary."""
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            extracted_text += f"\n--- Page {page_num} ---\n" + text
        else:
            images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, poppler_path=POPPLER_PATH)
            for image in images:
                extracted_text += f"\n--- Page {page_num} (OCR) ---\n" + extract_text_from_image(image)

    return extracted_text.strip()

def extract_text(file_path):
    """Determine file type and extract text accordingly."""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image = Image.open(file_path)
        return extract_text_from_image(image)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        return "Unsupported file format."

def main():
    file_paths = [
        r"C:\Users\MOHAMED\Downloads\med.pdf",
        r"C:\Users\MOHAMED\Downloads\Farag Elyan.pdf",
        r"C:\Users\MOHAMED\Downloads\Screenshot 2025-03-06 195532.png"
    ]
    
    for file in file_paths:
        print(f"Extracted text from: {file}\n")
        print(extract_text(file))
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    main()
