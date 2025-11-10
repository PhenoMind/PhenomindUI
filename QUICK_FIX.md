# 🚀 IMMEDIATE ACTION REQUIRED - Frontend Not Connected to Backend

## Problem
Your Vercel frontend is trying to connect to `http://localhost:5000` instead of your Render backend at `https://phenomind-backend-nt75.onrender.com`.

## ✅ Files Updated (Already Done)
1. ✅ Created `.env.production` with backend URL
2. ✅ Created `.env.development` for local development
3. ✅ Updated `vercel.json` with environment variable
4. ✅ Updated error messages to show correct backend URL
5. ✅ Improved CORS configuration in backend

## 🔧 REQUIRED STEPS (DO THIS NOW)

### Step 1: Set Environment Variable in Vercel (CRITICAL)

Go to your Vercel project:
1. Open https://vercel.com/dashboard
2. Select your `phenomind-ui` project
3. Click **Settings** → **Environment Variables**
4. Add this variable:
   ```
   Name: REACT_APP_API_URL
   Value: https://phenomind-backend-nt75.onrender.com
   Environment: Production ✓ Preview ✓
   ```
5. Click **Save**

### Step 2: Redeploy Frontend

After adding the environment variable, you MUST redeploy:

**Option A: Via Git (Recommended)**
```bash
cd /Users/shaksonisaac/Documents/GitHub/PhenomindUI
git add .
git commit -m "Fix: Connect frontend to Render backend"
git push origin main
```
Vercel will auto-deploy.

**Option B: Via Vercel Dashboard**
1. Go to your project → **Deployments**
2. Click the **three dots** (...) on the latest deployment
3. Click **Redeploy**

### Step 3: Verify Backend CORS Settings

In your Render dashboard:
1. Go to your backend service
2. Click **Environment**
3. Verify `CORS_ORIGINS` is set to: `https://phenomind-ui.vercel.app`
4. If it has a different URL or multiple URLs, update it to match your actual Vercel URL

### Step 4: Test the Connection

After redeployment:
1. Visit https://phenomind-ui.vercel.app
2. Open browser console (F12)
3. You should see API requests going to `https://phenomind-backend-nt75.onrender.com`
4. Patients should load successfully

## 🔍 Verification Checklist

- [ ] Environment variable `REACT_APP_API_URL` set in Vercel
- [ ] Frontend redeployed after setting variable
- [ ] Backend CORS allows your Vercel URL
- [ ] Can access https://phenomind-backend-nt75.onrender.com/api/patients directly
- [ ] Frontend shows patients (not connection error)

## 🐛 If Still Not Working

1. **Check Browser Console**
   - Open DevTools (F12) → Console tab
   - Look for API request URLs
   - Should see: `https://phenomind-backend-nt75.onrender.com/api/...`
   - If still seeing `localhost:5000`, the env variable didn't apply

2. **Check Network Tab**
   - Open DevTools (F12) → Network tab
   - Reload page
   - Click on the API request
   - Check if CORS error or 404

3. **Verify Backend is Running**
   ```bash
   curl https://phenomind-backend-nt75.onrender.com/health
   ```
   Should return: `{"status":"ok","message":"PhenoMind API is healthy"}`

4. **Check Render Logs**
   - Go to Render dashboard
   - Select backend service
   - Click **Logs** tab
   - Look for CORS or 404 errors

## 📝 Quick Test Commands

```bash
# Test backend health
curl https://phenomind-backend-nt75.onrender.com/health

# Test backend API
curl https://phenomind-backend-nt75.onrender.com/api/patients

# Should see JSON data, not HTML or error
```

## 🎯 Expected Result

After completing these steps:
- ✅ Frontend loads at https://phenomind-ui.vercel.app
- ✅ Patients list appears on the left sidebar
- ✅ No "Cannot connect to backend" errors
- ✅ Patient details load when clicking on a patient
- ✅ Charts and analytics display correctly

## 📚 Additional Resources

See `DEPLOYMENT.md` for complete deployment documentation.

---

**Need Help?**
If the issue persists after following these steps, check:
1. Vercel deployment logs
2. Render backend logs  
3. Browser console errors
4. Network tab in DevTools
