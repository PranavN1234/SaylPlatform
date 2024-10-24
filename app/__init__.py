from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.config import get_config  # Import the environment-based config selector

load_dotenv()  # Load environment variables

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load the appropriate config class (Development or Production)
    config = get_config()
    app.config.from_object(config)  # Apply the selected config

    # Add any additional configurations
    app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on filesystem
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

    # Debugging: Print environment and DB URI to ensure correctness
    print(f"Environment: {config.__name__}")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize extensions with the app context
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, origins="*")

    # Set up Flask-Migrate with the app and database
    migrate.init_app(app, db)

    # Register API blueprints
    from app.api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
