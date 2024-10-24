import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DEV_DB_NAME')}"
    )

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('PROD_DB_NAME')}"
    )

def get_config():
    """Return the appropriate config class based on the environment."""
    environment = os.getenv('ENVIRONMENT', 'development')
    if environment == 'production':
        return ProductionConfig
    return DevelopmentConfig

    
