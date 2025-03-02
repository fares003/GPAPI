from flask import Blueprint, request, jsonify
from controllers.ocr_controller import extract_text
from werkzeug.utils import secure_filename
import os

ocr_bp = Blueprint('ocr', __name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'  # Ensure this folder exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/extract_text', methods=['POST'])
def ocr_upload():
    """Handle file uploads and extract text based on file type."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Sanitize filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)  # Save uploaded file

        try:
            extracted_text = extract_text(filepath)  # Call OCR function
            os.remove(filepath)  # Clean up the uploaded file
            return jsonify({'text': extracted_text})  # Return extracted text
        except Exception as e:
            os.remove(filepath)  # Ensure deletion even if OCR fails
            return jsonify({'error': f'OCR failed: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, pdf, docx'}), 400
