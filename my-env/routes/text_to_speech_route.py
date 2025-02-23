from flask import Blueprint,request,jsonify,send_file

from controllers.text_to_speech import convert_text_to_speech

models_bp=Blueprint('models',__name__)

@models_bp.route("/text_to_speech", methods=["POST"])
def text_to_speech_api():
    """API endpoint that receives text, converts it to speech, and returns an audio file."""

    # Get JSON request data
    data = request.get_json()

    # Validate input
    if not data or "sentences" not in data:
        return jsonify({"error": "Sentences input is required!"}), 400

    sentences = data["sentences"]

    # Ensure it's a list of strings
    if not isinstance(sentences, list) or not all(isinstance(s, str) for s in sentences):
        return jsonify({"error": "Sentences must be a list of strings!"}), 400

    # Call the function to generate speech
    output_file = convert_text_to_speech(sentences)

    # Return the generated audio file
    return send_file(output_file, as_attachment=True)
