from flask import Flask
from routes.user_routes import user_bp
from routes.pdf_text_extraction_route import pdf_tools_bp
from routes.text_to_speech_route import models_bp
from routes.ocr_routes import ocr_bp  

app = Flask(__name__)

app.register_blueprint(user_bp,url_prefix='/users')
app.register_blueprint(pdf_tools_bp,url_prefix='/pdf_tools')
app.register_blueprint(models_bp,url_prefix='/models')
app.register_blueprint(ocr_bp, url_prefix='/ocr')




if __name__ == '__main__':
    app.run(debug=True)
# <<<<<<< khalil1

# import torch
# print("CUDA Available:", torch.cuda.is_available())
# print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")
# =======
# >>>>>>> khalilBranch
