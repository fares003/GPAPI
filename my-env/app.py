from flask import Flask
from routes.user_routes import user_bp
from routes.ocr_routes import ocr_bp  # Ensure the correct file name is used

app = Flask(__name__)

# Register user-related routes
app.register_blueprint(user_bp, url_prefix='/users')

# Register OCR-related routes
app.register_blueprint(ocr_bp, url_prefix='/ocr')

if __name__ == '__main__':
    app.run(debug=True)
