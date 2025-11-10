# PhenoMind Deployment Guide

## Overview
PhenoMind is deployed with:
- **Frontend**: Vercel (https://phenomind-ui.vercel.app)
- **Backend**: Render (https://phenomind-backend-nt75.onrender.com)
- **Database**: PostgreSQL on Render

## Frontend Configuration (Vercel)

### Environment Variables
The frontend needs to know where the backend API is located:

**Local Development:**
```bash
REACT_APP_API_URL=http://localhost:5000
```

**Production (Vercel):**
```bash
REACT_APP_API_URL=https://phenomind-backend-nt75.onrender.com
```

### Setting Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variable:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://phenomind-backend-nt75.onrender.com`
   - **Environments**: Production, Preview (optional)
4. Click **Save**
5. **Redeploy** your application for changes to take effect

### Alternative: Using vercel.json
The `vercel.json` file already includes the environment variable, but Vercel dashboard settings take precedence.

## Backend Configuration (Render)

### Environment Variables on Render
Already configured in `render.yaml`:
- `FLASK_ENV=production`
- `CORS_ORIGINS=https://phenomind-ui.vercel.app`
- `DATABASE_URL` (auto-generated from PostgreSQL)
- `SECRET_KEY` (auto-generated)

### CORS Configuration
The backend is configured to accept requests from:
- `https://phenomind-ui.vercel.app` (production)
- `http://localhost:3000` (local development)

If your Vercel URL changes, update the `CORS_ORIGINS` in Render:
1. Go to Render dashboard
2. Select your backend service
3. Go to **Environment** → Edit `CORS_ORIGINS`
4. Update the URL and save

## Database Setup

### Running Migrations on Render
After deploying, you need to populate the database:

1. Go to Render dashboard → Your backend service
2. Click **Shell** tab
3. Run:
   ```bash
   python migrate_data.py
   ```

This will create all tables and populate with 12 sample patients.

## Testing the Deployment

### Check Backend Health
```bash
curl https://phenomind-backend-nt75.onrender.com/health
```
Should return: `{"status":"ok","message":"PhenoMind API is healthy"}`

### Check Backend API
```bash
curl https://phenomind-backend-nt75.onrender.com/api/patients
```
Should return JSON array of patients.

### Check Frontend
Visit: https://phenomind-ui.vercel.app

## Common Issues

### Issue: "Cannot connect to backend server"
**Solution**: 
1. Verify `REACT_APP_API_URL` is set in Vercel environment variables
2. Redeploy the frontend after setting the variable
3. Clear browser cache

### Issue: CORS errors
**Solution**: 
1. Verify `CORS_ORIGINS` in Render includes your exact Vercel URL
2. Make sure there are no trailing slashes
3. Redeploy backend after changing CORS settings

### Issue: No patients showing
**Solution**: 
1. Check if backend returns data: `curl https://phenomind-backend-nt75.onrender.com/api/patients`
2. If empty, run migration script in Render shell
3. Check browser console for errors

### Issue: 500 errors from backend
**Solution**: 
1. Check Render logs: Dashboard → Logs
2. Verify database connection
3. Check if migrations were run

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python migrate_data.py  # First time only
python run.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

The frontend will automatically use `http://localhost:5000` in development mode.

## Production URLs

- **Frontend**: https://phenomind-ui.vercel.app
- **Backend API**: https://phenomind-backend-nt75.onrender.com
- **Backend Health**: https://phenomind-backend-nt75.onrender.com/health
- **API Endpoints**:
  - `/api/patients` - List all patients
  - `/api/patients/:id` - Get patient details
  - `/api/analytics/population` - Population analytics
  - `/api/analytics/forecast/:id` - Patient forecast

## Deployment Commands

### Deploy Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

Or push to your connected Git repository for auto-deployment.

### Deploy Backend (Render)
Push to your Git repository. Render will auto-deploy based on `render.yaml`.

## Monitoring

### Backend Logs
View in Render dashboard → Your service → Logs

### Frontend Logs  
View in Vercel dashboard → Your project → Deployments → [Select deployment] → Runtime Logs

### Health Check
The backend has a health check endpoint at `/health` that Render pings automatically.
