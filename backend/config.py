import os
from dotenv import load_dotenv

# Load .env from project root (one level up from backend/)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

class Config:
    """Base configuration"""
    # Get the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    
    # Ensure instance directory exists
    os.makedirs(instance_path, exist_ok=True)
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use instance folder for database (Flask convention)
    default_db_path = os.path.join(instance_path, 'phenomind.db')
    database_url = os.environ.get('DATABASE_URL') or f'sqlite:///{default_db_path}'
    
    # Fix for Render PostgreSQL URLs (postgres:// -> postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Parse CORS origins - supports comma-separated list
    cors_origins_str = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

