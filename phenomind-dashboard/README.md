# PhenoMind Dashboard

A full-stack mental health monitoring dashboard application with AI-powered insights.

## Project Structure

```
phenomind-dashboard/
├── backend/          # Flask REST API
│   ├── api/         # API routes/blueprints
│   ├── models/      # Database models
│   ├── services/    # Business logic
│   ├── config.py    # Configuration
│   ├── database.py  # Database initialization
│   └── run.py       # Entry point
│
├── frontend/         # React application
│   ├── src/         # Source code
│   ├── public/      # Static assets
│   └── package.json
│
└── docs/            # Documentation
    └── HOSTING_GUIDE.md
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python migrate_data.py
python run.py
```

Backend runs on `http://localhost:5001`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:5001
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///phenomind.db
CORS_ORIGINS=http://localhost:3000
```

## Documentation

- [Hosting Guide](./docs/HOSTING_GUIDE.md) - Deployment instructions
- [Backend README](./backend/README.md) - API documentation

## Tech Stack

**Backend:**
- Flask
- SQLAlchemy
- Flask-CORS
- Flask-Migrate

**Frontend:**
- React
- Tailwind CSS
- Recharts
- Framer Motion
- Radix UI
