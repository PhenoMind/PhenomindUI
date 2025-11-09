#!/usr/bin/env python3
"""
Startup script that verifies everything is set up correctly before starting the server
"""
import sys
import os

def check_setup():
    """Check if everything is set up correctly"""
    errors = []
    warnings = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        errors.append("Python 3.7+ required. Current version: " + sys.version)
    
    # Check if we're in the right directory
    if not os.path.exists('app'):
        errors.append("Cannot find 'app' directory. Make sure you're in the backend directory.")
    
    # Check if config exists
    if not os.path.exists('config.py'):
        errors.append("Cannot find 'config.py'. Make sure you're in the backend directory.")
    
    # Check if database file exists (warning, not error)
    if not os.path.exists('phenomind.db'):
        warnings.append("Database file 'phenomind.db' not found. It will be created on first run.")
    
    # Try importing
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            db.create_all()
        print("✓ All imports successful")
    except ImportError as e:
        errors.append(f"Import error: {e}. Run: pip install -r requirements.txt")
    except Exception as e:
        errors.append(f"Error creating app: {e}")
    
    # Print results
    if errors:
        print("\n❌ ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("\n✓ Setup looks good! Starting server...\n")
    return True

if __name__ == '__main__':
    if not check_setup():
        print("\nPlease fix the errors above before starting the server.")
        sys.exit(1)
    
    # Start the server
    from app import create_app
    app = create_app()
    
    print("=" * 50)
    print("PhenoMind API Server")
    print("=" * 50)
    print("Server running on: http://localhost:5000")
    print("API endpoints:")
    print("  - GET  /                    Health check")
    print("  - GET  /api                 API info")
    print("  - GET  /api/patients         Get all patients")
    print("  - GET  /api/patients/<id>    Get patient by ID")
    print("  - GET  /api/patients/<id>/analytics  Get patient analytics")
    print("=" * 50)
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

