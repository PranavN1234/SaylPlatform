from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    CORS(app, supports_credentials=True, origins="*")    
    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app