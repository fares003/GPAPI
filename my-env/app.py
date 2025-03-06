from flask import Flask
from routes.user_routes import user_bp
from routes.ocr_routes import ocr_bp  
from routes.translate_routes import translate_bp


app = Flask(__name__)

# Register user-related routes
app.register_blueprint(user_bp, url_prefix='/users')

# Register OCR-related routes
app.register_blueprint(ocr_bp, url_prefix='/ocr')

# ✅ Register Translation-related routes
app.register_blueprint(translate_bp, url_prefix='/translate')  # ✅ Ensure this is here

if __name__ == '__main__':
    app.run(debug=True)
