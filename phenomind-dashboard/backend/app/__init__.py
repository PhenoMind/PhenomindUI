from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # Allow all origins in development for easier debugging
    if app.config.get('DEBUG'):
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    else:
        CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes import patients_bp, analytics_bp
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    
    # Add a simple health check route
    @app.route('/')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'PhenoMind API is running'})
    
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

