from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from database import db
from api import patients_bp, analytics_bp

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

