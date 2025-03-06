import fitz  # PyMuPDF
import pytesseract  # Import Tesseract OCR for text recognition from images
import cv2  # OpenCV for image processing
import numpy as np  # NumPy for numerical operations (used in image processing)
from docx import Document  # Import python-docx to extract text from DOCX files
from PIL import Image  # Import Pillow for image manipulation
import os  # Import OS module for file operations
import io

# Set the path to Tesseract OCR executable (ensure this matches your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image to enhance OCR accuracy by applying grayscale, thresholding, and blurring."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 31, 2)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return gray

def extract_text_from_image(image_path):
    """Extract text from an image file using Tesseract OCR."""
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, lang='eng')
    return " ".join(text.splitlines())

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file using python-docx."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

""" def extract_text_from_pdf(pdf_path):
    ""Extract text from a PDF file, using OCR if necessary."
    doc = fitz.open(pdf_path)
    extracted_text = ""
    
    for page in doc:
        text = page.get_text("text")
        if text.strip():
            extracted_text += text + "\n"
        else:
            pix = page.get_pixmap()
            image_path = "temp_page.png"
            Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(image_path)
            extracted_text += extract_text_from_image(image_path) + "\n"
            os.remove(image_path)
    
    return extracted_text.strip() """
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file, handling both selectable text and images."""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text("text") + "\n"
        
        # If no text is found, try OCR
        if not page.get_text("text").strip():
            images = convert_from_path(pdf_path, first_page=page.number+1, last_page=page.number+1)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
    
    return text

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

def main():
    file_paths = [
        r"C:\Users\MOHAMED\Desktop\pdf tests\tests\test4.pdf",
        r"C:\Users\MOHAMED\Downloads\Farag Elyan.pdf",
        r"C:\Users\MOHAMED\Desktop\Image_Tests\Tests\ts7.png",
        r"C:\Users\MOHAMED\Downloads\MS1 Appendix.docx"
    ]
    
    for file in file_paths:
        print(f"Extracted text from: {file}\n")
        print(extract_text(file))
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    main()
