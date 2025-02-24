from flask import Blueprint, request, jsonify, render_template
from controllers.ocr_controller import extract_text_from_image
from werkzeug.utils import secure_filename
import os

ocr_bp = Blueprint('ocr', __name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'  # Create this folder in your project
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route('/Add_ocr', methods=['POST'])
def ocr_upload():
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #Sanitize filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                extracted_text = extract_text_from_image(filepath)
                os.remove(filepath)  # Clean up uploaded file

                return jsonify({'text': extracted_text})
            except Exception as e:
                os.remove(filepath) # Ensure deletion even if OCR fails
                return jsonify({'error': f'OCR failed: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg'}), 400

    # For GET requests, render the upload form
   