import pytesseract 
import cv2 
import numpy as np 
 
# Set Tesseract path (if not set automatically) 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 
 
def preprocess_image(image_path): 
    """Preprocess the image to improve OCR accuracy.""" 
    # Load the image 
    image = cv2.imread(image_path) 
 
    # Convert to grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
 
    # Apply adaptive thresholding to improve contrast 
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 31, 2) 
 
    # Apply slight Gaussian blur to reduce noise 
    gray = cv2.GaussianBlur(gray, (3, 3), 0) 
 
    # Save preprocessed image for debugging (optional) 
    processed_image_path = image_path.replace(".png", "_processed.png") 
    cv2.imwrite(processed_image_path, gray) 
 
    return gray, processed_image_path 
 
def extract_text_from_image(image_path): 
    """Extract text from an image using Tesseract OCR.""" 
    # Preprocess the image 
    processed_image, processed_image_path = preprocess_image(image_path) 
 
    # Extract text 
    text = pytesseract.image_to_string(processed_image, lang='eng') 

    # Remove unnecessary newlines while keeping paragraph structure
    cleaned_text = " ".join(text.splitlines())

    return cleaned_text
