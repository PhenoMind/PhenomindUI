# Hosting Guide - React + Flask Architecture

## How It Works

Your application has **two separate parts** that need to be hosted:

### 1. **Frontend (React)** - Port 3000 (development)
- This is what users see in their browser
- Contains all the UI components, styling, and user interactions
- Makes API calls to the backend to get data
- **In production**: Built into static files (HTML, CSS, JS) that can be served by any web server

### 2. **Backend (Flask API)** - Port 5000 (development)
- This is the server that handles data, business logic, and analytics
- Provides REST API endpoints (like `/api/patients`)
- Connects to the database
- **In production**: Runs as a Python application on a server

## Development Setup (What You Have Now)

```
┌─────────────────┐         HTTP Requests         ┌─────────────────┐
│                 │  http://localhost:3000        │                 │
│  React App      │ ────────────────────────────> │  Flask API      │
│  (Frontend)     │                                │  (Backend)      │
│  Port 3000      │ <────────────────────────────  │  Port 5000      │
│                 │      JSON Responses           │                 │
└─────────────────┘                                └─────────────────┘
                                                           │
                                                           ▼
                                                    ┌─────────────────┐
                                                    │   SQLite DB     │
                                                    │  phenomind.db   │
                                                    └─────────────────┘
```

**How to run:**
1. **Terminal 1**: `cd backend && python run.py` (starts Flask on port 5000)
2. **Terminal 2**: `npm start` (starts React on port 3000)
3. Open browser: `http://localhost:3000`

## Production Hosting Options

### Option 1: Separate Hosting (Recommended for Learning)

**Frontend (React):**
- **Vercel** (easiest, free)
- **Netlify** (free)
- **GitHub Pages** (free)
- **AWS S3 + CloudFront** (paid)

**Backend (Flask):**
- **Heroku** (free tier available)
- **Railway** (free tier)
- **Render** (free tier)
- **AWS EC2** (paid)
- **DigitalOcean** (paid)

### Option 2: Same Server (Traditional)

Host both on one server:
- **AWS EC2**
- **DigitalOcean Droplet**
- **Linode**
- **Your own server**

## Step-by-Step: Deploy to Vercel (Frontend) + Render (Backend)

### Part 1: Deploy Backend to Render (Free)

1. **Prepare your backend:**
   ```bash
   cd backend
   # Make sure you have a requirements.txt (you do!)
   ```

2. **Create a `Procfile` for Render:**
   ```bash
   echo "web: gunicorn run:app" > Procfile
   ```

3. **Update requirements.txt to include gunicorn:**
   ```
   gunicorn==21.2.0
   ```

4. **Go to Render.com:**
   - Sign up (free)
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn run:app`
     - Environment: Python 3
   - Add environment variables:
     - `FLASK_ENV=production`
     - `DATABASE_URL=sqlite:///phenomind.db` (or use PostgreSQL)
     - `CORS_ORIGINS=https://your-frontend.vercel.app`

5. **Get your backend URL:** `https://your-app.onrender.com`

### Part 2: Deploy Frontend to Vercel (Free)

1. **Create `.env.production` file:**
   ```bash
   REACT_APP_API_URL=https://your-app.onrender.com
   ```

2. **Update `src/services/api.js` to use environment variable:**
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
   ```
   (This is already done!)

3. **Go to Vercel.com:**
   - Sign up (free)
   - Click "New Project"
   - Import your GitHub repo
   - Settings:
     - Framework Preset: Create React App
     - Root Directory: `./` (root of your project)
     - Environment Variables:
       - `REACT_APP_API_URL`: `https://your-app.onrender.com`
   - Deploy!

4. **Get your frontend URL:** `https://your-app.vercel.app`

### Part 3: Update CORS

Update your backend `config.py`:
```python
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
# Add your Vercel URL to the list
```

## How It Works in Production

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Browser                            │
│                                                              │
│  Opens: https://your-app.vercel.app                         │
│  ↓                                                           │
│  Loads React app (HTML, CSS, JS files)                       │
│  ↓                                                           │
│  React app makes API calls to:                             │
│  https://your-app.onrender.com/api/patients                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Vercel (Frontend Hosting)                      │
│  - Serves static files (React build)                         │
│  - Fast CDN worldwide                                       │
└─────────────────────────────────────────────────────────────┘

                          │
                          │ HTTPS API Calls
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Render (Backend Hosting)                       │
│  - Runs Flask application                                   │
│  - Handles API requests                                     │
│  - Connects to database                                     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Comparison

| Aspect | Development | Production |
|--------|------------|------------|
| **Frontend** | `npm start` (port 3000) | Built static files on CDN |
| **Backend** | `python run.py` (port 5000) | Running on cloud server |
| **Database** | Local SQLite file | Cloud database (PostgreSQL) |
| **URLs** | localhost:3000, localhost:5000 | your-app.vercel.app, your-app.onrender.com |
| **CORS** | localhost:3000 | your-app.vercel.app |

## Important Notes

1. **Environment Variables:**
   - Frontend: `REACT_APP_API_URL` must point to your backend URL
   - Backend: `CORS_ORIGINS` must include your frontend URL

2. **Database:**
   - SQLite works for development
   - For production, use PostgreSQL (Render provides this free)

3. **Build Process:**
   - Frontend: `npm run build` creates optimized static files
   - Backend: Just needs Python and dependencies

4. **Free Tier Limits:**
   - Vercel: Unlimited for personal projects
   - Render: Free tier spins down after 15 min inactivity (first request is slow)

## Alternative: Single Server Deployment

If you want everything on one server:

1. **Build React app:**
   ```bash
   npm run build
   ```

2. **Serve static files from Flask:**
   ```python
   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve(path):
       if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
           return send_from_directory(app.static_folder, path)
       else:
           return send_from_directory(app.static_folder, 'index.html')
   ```

3. **Deploy to one server** (Heroku, Railway, etc.)

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/

