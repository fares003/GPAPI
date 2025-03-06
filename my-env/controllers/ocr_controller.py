from flask import Blueprint
import pytesseract  # Tesseract OCR for text recognition
import cv2  # OpenCV for image processing
import fitz  # PyMuPDF for handling PDFs
from docx import Document  # python-docx for DOCX text extraction
from PIL import Image  # Pillow for image handling
import os  # OS for file operations
import numpy as np

# Set Tesseract OCR path (ensure it matches your installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define a Flask Blueprint for the OCR controller
ocr_controller = Blueprint("ocr_controller", __name__)

def preprocess_image(image_path):
    """Preprocess image for better OCR accuracy."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return gray

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, lang='eng')
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF, handling both text-based and image-based content."""
    doc = fitz.open(pdf_path)
    extracted_text = ""
    
    for page in doc:
        text = page.get_text("text")
        if text.strip():  # If text is selectable, use it
            extracted_text += text + "\n"
        else:  # If it's an image-based PDF, apply OCR
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            temp_image_path = "temp_image.png"
            img.save(temp_image_path)
            extracted_text += extract_text_from_image(temp_image_path) + "\n"
            os.remove(temp_image_path)
    
    return extracted_text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_text(file_path):
    """Determine file type and extract text accordingly."""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        return extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."
