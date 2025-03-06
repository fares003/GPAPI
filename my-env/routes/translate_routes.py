from flask import Blueprint, request, jsonify
from controllers.translate_controller import translate_text

translate_bp = Blueprint("translate", __name__)  # ✅ Correct Blueprint name

@translate_bp.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    src_lang = data.get("src_lang", "")
    tgt_lang = data.get("tgt_lang", "")

    if not text or not src_lang or not tgt_lang:
        return jsonify({"error": "Missing required fields"}), 400

    translation = translate_text(text, src_lang, tgt_lang)
    return jsonify({"translation": translation})

