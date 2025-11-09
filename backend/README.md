# PhenoMind Backend API

Flask REST API for the PhenoMind dashboard application.

## Setup

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Initialize the database:**
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

4. **Migrate patient data:**
```bash
python migrate_data.py
```

5. **Run the Flask server:**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Patients
- `GET /api/patients` - Get all patients (optional `?search=query` parameter)
- `GET /api/patients/<id>` - Get a specific patient
- `POST /api/patients` - Create a new patient
- `PUT /api/patients/<id>` - Update a patient
- `DELETE /api/patients/<id>` - Delete a patient

### Analytics
- `GET /api/patients/<id>/analytics` - Get analytics for a specific patient
- `GET /api/analytics/population` - Get population-level analytics
- `GET /api/analytics/risk-distribution` - Get risk score distribution
- `GET /api/analytics/disorder-breakdown` - Get breakdown by disorder type

## Database

The application uses SQLite by default (for development). For production, update `DATABASE_URL` in `.env` to use PostgreSQL.

## Development

To run in development mode with auto-reload:
```bash
export FLASK_ENV=development
python run.py
```

