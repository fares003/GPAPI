import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os

# Set Tesseract path (modify based on your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image to improve OCR accuracy."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    processed_image_path = image_path.replace(".png", "_processed.png").replace(".jpg", "_processed.jpg")
    cv2.imwrite(processed_image_path, gray)
    
    return processed_image_path

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    processed_image_path = preprocess_image(image_path)
    text = pytesseract.image_to_string(Image.open(processed_image_path), lang='eng')
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file by converting each page to an image."""
    pages = convert_from_path(pdf_path, dpi=300)
    extracted_text = ""

    for i, page in enumerate(pages):
        image_path = f"page_{i+1}.png"
        page.save(image_path, "PNG")

        text = extract_text_from_image(image_path)
        extracted_text += f"\n--- Page {i+1} ---\n{text}\n"
        
        os.remove(image_path)  # Clean up temporary image file

    return extracted_text

# Main Execution
file_path = input("Enter the image or PDF file path: ").strip('"')

if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
    text = extract_text_from_image(file_path)
    print("\nExtracted Text from Image:\n", text)

elif file_path.lower().endswith('.pdf'):
    text = extract_text_from_pdf(file_path)
    print("\nExtracted Text from PDF:\n", text)

else:
    print("Unsupported file format. Please provide a PNG, JPG, or PDF file.")
