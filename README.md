# PhenoMind Dashboard

A full-stack mental health monitoring dashboard application with AI-powered insights and patient analytics.

## 🎯 Features

- **Patient Management**: View and search through patient records with detailed health information
- **AI-Powered Insights**: Personalized risk assessments and biomarker analysis for each patient
- **Real-time Analytics**: Track sleep, HRV, activity, and mood trends over time
- **Treatment Recommendations**: AI-generated recommendations based on patient data
- **Interactive Chatbot**: Patient-specific assistant for quick information access
- **Population Analytics**: Overview of patient population health metrics

## 📁 Project Structure

```
phenomind-dashboard/
├── backend/              # Flask REST API
│   ├── api/             # API routes/blueprints
│   │   ├── patients.py  # Patient endpoints
│   │   └── analytics.py # Analytics endpoints
│   ├── models/          # Database models
│   │   ├── patient.py
│   │   ├── ehr.py
│   │   ├── wearable.py
│   │   ├── timeline.py
│   │   └── trend_data.py
│   ├── services/        # Business logic
│   │   └── analytics_service.py
│   ├── instance/        # Instance-specific files (database)
│   │   └── phenomind.db
│   ├── config.py        # Configuration
│   ├── database.py      # Database initialization
│   ├── app.py           # Flask app factory
│   ├── run.py           # Entry point
│   ├── migrate_data.py  # Data migration script
│   └── requirements.txt
│
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── services/    # API service
│   │   └── PhenomindDashboard.jsx
│   ├── public/          # Static assets
│   ├── .env             # Frontend environment variables
│   └── package.json
│
├── docs/                # Documentation
│   └── HOSTING_GUIDE.md
│
└── .env                 # Root environment variables
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the database migration:
```bash
python migrate_data.py
```

5. Start the backend server:
```bash
python run.py
```

The backend will run on `http://localhost:5001` (or `http://localhost:5000` if 5001 is unavailable).

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

## ⚙️ Environment Variables

### Root `.env` File

Create a `.env` file in the project root:

```env
# Frontend API URL
REACT_APP_API_URL=http://localhost:5001

# Backend Configuration
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///phenomind.db
CORS_ORIGINS=http://localhost:3000
```

### Frontend `.env` File

Create a `.env` file in the `frontend/` directory (React apps read `.env` from their own directory):

```env
REACT_APP_API_URL=http://localhost:5001
```

**Note**: The frontend `.env` file is required for Create React App to read environment variables.

## 🗄️ Database

The application uses SQLite by default (stored in `backend/instance/phenomind.db`). 

- **Location**: `backend/instance/phenomind.db`
- **Migration**: Run `python backend/migrate_data.py` to populate with sample patient data
- **Production**: Update `DATABASE_URL` in `.env` to use PostgreSQL or another database

## 🎨 Features Overview

### Patient Dashboard
- View patient demographics and risk scores
- Track biomarker trends (sleep, HRV, activity, mood)
- Review EHR data and wearable device information
- View patient timeline of events

### AI Insights
- **Biomarker Drivers**: Visual breakdown of factors affecting patient risk
- **Treatment Recommendations**: Personalized recommendations with priority levels
- **Risk Analysis**: Patient-specific relapse risk assessment

### Interactive Chatbot
- Click the chat icon in the bottom-right corner
- Ask questions about the selected patient:
  - "What is the patient's risk level?"
  - "Tell me about their sleep patterns"
  - "What medications are they on?"
  - "What are the recommendations?"
  - "What is their diagnosis?"

### Population Analytics
- Overview of all patients
- Risk distribution across the population
- Disorder breakdown statistics

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Migrate** - Database migrations
- **python-dotenv** - Environment variable management

### Frontend
- **React** - UI library
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Radix UI** - Accessible component primitives
- **Lucide React** - Icons

## 📚 API Endpoints

### Patients
- `GET /api/patients` - Get all patients
- `GET /api/patients/:id` - Get patient by ID
- `GET /api/patients/:id/analytics` - Get patient analytics

### Analytics
- `GET /api/analytics/population` - Population-level analytics
- `GET /api/analytics/risk-distribution` - Risk score distribution
- `GET /api/analytics/disorder-breakdown` - Breakdown by disorder type

## 🧪 Development

### Running in Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

The build output will be in `frontend/build/`.

## 📖 Documentation

- [Hosting Guide](./docs/HOSTING_GUIDE.md) - Deployment instructions
- [Backend README](./backend/README.md) - Detailed API documentation

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Ensure the backend is running on port 5001 (or 5000)
- Check that `REACT_APP_API_URL` in `frontend/.env` matches the backend port
- Restart the React dev server after changing `.env` files

### No patients found
- Run the migration script: `python backend/migrate_data.py`
- Check that the database file exists in `backend/instance/`

### Port already in use
- Backend will automatically try port 5001 if 5000 is unavailable
- Update `REACT_APP_API_URL` accordingly

## 📝 License

This project is for demonstration purposes.

## 🤝 Contributing

This is a private project. For questions or issues, please contact the development team.
