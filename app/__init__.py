from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.routes import main
    app.register_blueprint(main)

    return app