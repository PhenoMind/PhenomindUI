#!/bin/bash

# Setup script for PhenoMind backend

echo "Setting up PhenoMind backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Initialize database
echo "Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"

echo ""
echo "Setup complete!"
echo ""
echo "To run the server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run migration: python migrate_data.py"
echo "  3. Start server: python run.py"
echo ""

