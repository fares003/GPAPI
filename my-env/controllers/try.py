import pytesseract  # Import Tesseract OCR for text recognition from images
import cv2  # OpenCV for image processing
import numpy as np  # NumPy for numerical operations (used in image processing)
import fitz  # PyMuPDF for handling PDF files and extracting images from them
from docx import Document  # Import python-docx to extract text from DOCX files
from PIL import Image  # Import Pillow for image manipulation
import os  # Import OS module for file operations

# Set the path to Tesseract OCR executable (ensure this matches your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image to enhance OCR accuracy by applying grayscale, thresholding, and blurring."""
    image = cv2.imread(image_path)  # Read the image from the given file path
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 31, 2)  # Apply adaptive thresholding to improve contrast
    gray = cv2.GaussianBlur(gray, (3, 3), 0)  # Apply Gaussian blur to reduce noise
    processed_image_path = image_path.replace(".png", "_processed.png")  # Save processed image path for debugging
    cv2.imwrite(processed_image_path, gray)  # Save the processed image (optional step for debugging)
    return gray  # Return the processed grayscale image

def extract_text_from_image(image_path):
    """Extract text from an image file using Tesseract OCR."""
    processed_image = preprocess_image(image_path)  # Preprocess the image before applying OCR
    text = pytesseract.image_to_string(processed_image, lang='eng')  # Use Tesseract OCR to extract text from the image
    return " ".join(text.splitlines())  # Clean up extracted text by removing unnecessary newlines

def extract_text_from_pdf_images(pdf_path):
    """Extract text from a scanned PDF by converting each page into an image and applying OCR."""
    doc = fitz.open(pdf_path)  # Open the PDF file using PyMuPDF
    text = ""  # Initialize an empty string to store extracted text
    for i, page in enumerate(doc):  # Iterate through each page of the PDF
        pix = page.get_pixmap()  # Render the page as an image
        image_path = f"temp_page_{i}.png"  # Define a temporary file name for the extracted image
        Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(image_path)  # Save the image file
        text += extract_text_from_image(image_path) + "\n"  # Extract text from the image and append to the result
        os.remove(image_path)  # Delete the temporary image file after processing
    return text.strip()  # Return the extracted text with unnecessary spaces removed

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file using python-docx."""
    doc = Document(docx_path)  # Open the DOCX file
    return "\n".join([para.text for para in doc.paragraphs]).strip()  # Extract and return the text from all paragraphs

def extract_text(file_path):
    """Determine file type and extract text accordingly."""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Check if the file is an image
        return extract_text_from_image(file_path)  # Extract text from the image
    elif file_path.lower().endswith('.pdf'):  # Check if the file is a PDF
        return extract_text_from_pdf_images(file_path)  # Extract text from the PDF using OCR on its images
    elif file_path.lower().endswith('.docx'):  # Check if the file is a DOCX document
        return extract_text_from_docx(file_path)  # Extract text from the DOCX file
    else:
        return "Unsupported file format."  # Return a message if the file format is not supported

# Example usage (testing the functions with sample files)
if __name__ == "__main__":
    pdf_text = extract_text(r"C:\Users\HP\Desktop\Screenshot 2025-03-03 010947.png")  # Extract text from a sample PDF file
    print("Extracted text from PDF using Tesseract:\n", pdf_text)  # Print extracted text from PDF
    
    # docx_text = extract_text(r"C:\Users\MOHAMED\Desktop\pdf tests\lables\L5.docx")  # Extract text from a sample DOCX file
    # print("\nExtracted text from DOCX:\n", docx_text)  # Print extracted text from DOCX
    
    # image_text = extract_text(r"C:\Users\MOHAMED\Desktop\Image_Tests\Tests\ts7.png")  # Extract text from a sample image file
    # print("\nExtracted text from Image:\n", image_text)  # Print extracted text from image