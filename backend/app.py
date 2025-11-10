from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from database import db
from api import patients_bp, analytics_bp
import os

migrate = Migrate()

def create_app(config_name=None):
    # Auto-detect environment if not specified
    if config_name is None:
        config_name = 'production' if os.environ.get('FLASK_ENV') == 'production' else 'development'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS
    cors_origins = app.config['CORS_ORIGINS']
    if app.config.get('DEBUG'):
        # Allow all origins in development
        CORS(app, resources={r"/*": {"origins": "*"}})
    else:
        # Use specific origins in production
        CORS(app, resources={r"/*": {"origins": cors_origins}})
    
    # Register blueprints
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    
    # Add a simple health check route
    @app.route('/')
    def home():
        return jsonify({'status': 'ok', 'message': 'PhenoMind API is running'})
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'PhenoMind API is healthy'})
    
    @app.route('/api')
    def api_info():
        return jsonify({
            'status': 'ok',
            'endpoints': {
                'patients': '/api/patients',
                'analytics': '/api/analytics'
            }
        })
    
    return app

