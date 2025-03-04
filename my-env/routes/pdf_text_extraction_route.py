from flask import Blueprint,request,jsonify

from controllers.pdf_text_extraction_controler import extract_text_from_pdf

pdf_tools_bp=Blueprint('pdf_tools',__name__)

@pdf_tools_bp.route('/extract_text', methods=['POST'])
def extract_text():
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['file']

    # Check if the uploaded file is a PDF
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    try:
        # Extract text from the uploaded PDF file
        extracted_sentences = extract_text_from_pdf(pdf_file)
        return jsonify({"extracted_text": extracted_sentences})

    except Exception as e:

        return jsonify({"error": str(e)}), 500

