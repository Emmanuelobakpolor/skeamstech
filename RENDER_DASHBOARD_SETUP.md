# How to Deploy on Render.com - Complete Setup Guide

## Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started" (top right)
3. Click "Sign up with GitHub" (easiest)
4. Authorize Render to access your GitHub
5. Verify your email
6. ✅ Account created!

---

## Step 2: Create PostgreSQL Database on Render

### 2a. Start Database Creation

1. Go to https://render.com/dashboard
2. Click **"New +"** (top left)
3. Select **"PostgreSQL"**

### 2b. Configure Database

Fill in these fields:

| Field | Value | Example |
|-------|-------|---------|
| **Name** | Your database name | `acked-postgres` |
| **Database** | Database name | `ackeddb` |
| **User** | Database user | `ackeddb_user` |
| **Region** | Choose closest to you | Oregon / us-west |
| **PostgreSQL Version** | Latest version | 15 or 16 |
| **Plan** | Free tier is fine | Free tier |

### 2c. Create Database

1. Click **"Create Database"**
2. Wait 1-2 minutes for creation
3. ✅ Database created!

### 2d. Save Database Credentials

Once created, you'll see:

```
INTERNAL DATABASE URL
postgresql://username:password@hostname:5432/ackeddb

Hostname: dpg-xxxxxxxxxxxxx.render.com
Database: ackeddb
User: ackeddb_user
Password: [shown once - SAVE IT!]
Port: 5432
```

**SAVE ALL THESE VALUES!** You'll need them.

---

## Step 3: Create Web Service (Django App)

### 3a. Start Service Creation

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Select **"Build and deploy from a Git repository"**

### 3b. Connect GitHub

1. Click **"Connect GitHub"**
2. Search for your repository (e.g., "tech" or "acked")
3. Click **"Connect"**

### 3c. Configure Service Settings

Fill in these fields:

| Field | Value | Example |
|-------|-------|---------|
| **Name** | Service name | `acked-backend` |
| **Environment** | Select Python | Python 3 |
| **Root Directory** | Where Django is | `acked/` |
| **Build Command** | How to build | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | How to run | `gunicorn acked.wsgi:application --bind 0.0.0.0:$PORT` |

### 3d. Choose Plan

- **Free tier:** Good for testing
- **Paid tier:** For production (auto-scales)

### 3e. Create Service

1. Click **"Create Web Service"**
2. Render starts building (takes 3-5 minutes)
3. You can watch the build logs

### 3f. Wait for Build

- Status shows: "Building..." 
- Then "Deploy in progress"
- Finally "Live" (green status)

**This takes 3-5 minutes!**

---

## Step 4: Add Environment Variables

### 4a. Access Environment Settings

1. Go to your Web Service dashboard
2. Click on **"acked-backend"** service
3. Go to **"Environment"** tab (left sidebar)

### 4b. Add Each Variable

Click **"Add Environment Variable"** and add these 14 variables:

### Group 1: Django Settings

**1. SECRET_KEY**
- Click "Add Environment Variable"
- Key: `SECRET_KEY`
- Value: Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Click "Save"

**2. DEBUG**
- Key: `DEBUG`
- Value: `False`
- Click "Save"

**3. ALLOWED_HOSTS**
- Key: `ALLOWED_HOSTS`
- Value: `acked-backend.onrender.com,localhost`
- (Replace "acked-backend" with your service name)
- Click "Save"

### Group 2: PostgreSQL Database

**4. DB_ENGINE**
- Key: `DB_ENGINE`
- Value: `django.db.backends.postgresql`
- Click "Save"

**5. DB_NAME**
- Key: `DB_NAME`
- Value: `ackeddb` (from Step 2)
- Click "Save"

**6. DB_USER**
- Key: `DB_USER`
- Value: `ackeddb_user` (from Step 2)
- Click "Save"

**7. DB_PASSWORD**
- Key: `DB_PASSWORD`
- Value: Your PostgreSQL password (from Step 2)
- Click "Save"

**8. DB_HOST**
- Key: `DB_HOST`
- Value: `dpg-xxxxxxxxxxxxx.render.com` (from Step 2)
- Click "Save"

**9. DB_PORT**
- Key: `DB_PORT`
- Value: `5432`
- Click "Save"

### Group 3: Cloudinary

**10. CLOUDINARY_CLOUD_NAME**
- Key: `CLOUDINARY_CLOUD_NAME`
- Value: Your Cloudinary Cloud Name
- (Get from: https://cloudinary.com/console/settings)
- Click "Save"

**11. CLOUDINARY_API_KEY**
- Key: `CLOUDINARY_API_KEY`
- Value: Your Cloudinary API Key
- Click "Save"

**12. CLOUDINARY_API_SECRET**
- Key: `CLOUDINARY_API_SECRET`
- Value: Your Cloudinary API Secret
- Click "Save"

### Group 4: Security

**13. CORS_ALLOWED_ORIGINS**
- Key: `CORS_ALLOWED_ORIGINS`
- Value: `http://localhost:3000,http://localhost:3001,https://your-frontend.vercel.app`
- (Multiple URLs separated by comma)
- Click "Save"

**14. CSRF_TRUSTED_ORIGINS**
- Key: `CSRF_TRUSTED_ORIGINS`
- Value: `https://your-frontend.vercel.app`
- (Your frontend URL)
- Click "Save"

### 4c. Auto-Redeploy

After adding variables:
- Service automatically redeploys
- Watch the "Logs" tab for deployment progress
- Wait for "Live" status (green)

**This takes 1-2 minutes!**

---

## Step 5: Run Migrations

### 5a. Open Shell

1. In your Web Service dashboard
2. Click **"Shell"** tab (left sidebar)
3. Click **"Connect"**

### 5b. Run Migration Command

In the web terminal, type:
```bash
python manage.py migrate
```

Wait for output like:
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying admin.0001_initial... OK
  Applying shop.0001_initial... OK
  etc.
```

✅ Migrations complete!

---

## Step 6: Test Your Backend

### 6a. Get Your Service URL

In Render dashboard, find your service URL:
```
https://acked-backend.onrender.com
```

### 6b. Test API Endpoints

Visit in browser:

**Test 1: Categories API**
```
https://acked-backend.onrender.com/shop/categories/
```
Should return JSON with categories

**Test 2: Products API**
```
https://acked-backend.onrender.com/shop/products/
```
Should return JSON with products

**Test 3: Check Logs**
```
In Render dashboard → Logs tab
Should see 200 responses (success)
```

### 6c: If Something's Wrong

Check **Logs** tab:
1. Go to Web Service dashboard
2. Click **"Logs"** tab
3. Scroll to see error messages
4. Fix the issue locally
5. Push to GitHub
6. Render auto-redeploys

---

## Complete Render Settings Visual

### Dashboard Layout

```
RENDER DASHBOARD
├─ Your Web Service (acked-backend)
│  ├─ Overview tab
│  │  └─ Shows: Status (Live), URL, Memory, CPU
│  ├─ Environment tab
│  │  └─ Shows: All 14 environment variables
│  ├─ Logs tab
│  │  └─ Shows: Build logs & runtime logs
│  ├─ Shell tab
│  │  └─ Connect to run commands
│  └─ Settings tab
│     └─ Service configuration
│
└─ PostgreSQL Instance (acked-postgres)
   ├─ Connections
   │  └─ Shows: Host, Database, User, Password
   └─ Logs tab
      └─ Database connection logs
```

---

## Settings Summary

### Web Service Settings (Render Dashboard)

| Setting | Value |
|---------|-------|
| **Service Name** | acked-backend |
| **Region** | Your chosen region |
| **Environment** | Python 3 |
| **Root Directory** | acked/ |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn acked.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | Free (or Starter) |
| **Status** | Live (green) |

### PostgreSQL Settings (Render Dashboard)

| Setting | Value |
|---------|-------|
| **Service Name** | acked-postgres |
| **Region** | Same as Web Service |
| **Database** | ackeddb |
| **User** | ackeddb_user |
| **PostgreSQL Version** | 15 or 16 |
| **Plan** | Free tier |

### Environment Variables (14 total)

See Step 4 above for all 14 variables.

---

## Deployment Checklist

- [ ] Created Render account
- [ ] Created PostgreSQL database
- [ ] Saved database credentials
- [ ] Created Web Service
- [ ] Connected GitHub repository
- [ ] Set Root Directory to `acked/`
- [ ] Set Build Command
- [ ] Set Start Command
- [ ] Added 14 environment variables
- [ ] Service shows "Live" (green)
- [ ] Ran migrations
- [ ] Tested API endpoints
- [ ] Checked logs for errors

---

## Your Final URLs

After deployment:

```
Frontend:    https://your-frontend.vercel.app
Backend API: https://acked-backend.onrender.com
Categories:  https://acked-backend.onrender.com/shop/categories/
Products:    https://acked-backend.onrender.com/shop/products/
```

---

## Common Issues & Fixes

### Service shows "Build Failed"

1. Check "Logs" tab for error
2. Common issues:
   - `requirements.txt` not found → Check Root Directory
   - Missing import → Fix code locally
   - Syntax error → Fix and push to GitHub

**Fix:** Push corrected code to GitHub, Render auto-redeploys

### "Internal Server Error" (500)

1. Check "Logs" tab
2. Common issues:
   - Environment variable missing → Add it
   - Database connection failed → Check DB credentials
   - Migration not applied → Run migration in Shell

**Fix:** Add variable or fix setting, service auto-redeploys

### Images not uploading

1. Check Cloudinary credentials
2. Verify CLOUDINARY_CLOUD_NAME is set
3. Test Cloudinary directly

**Fix:** Verify credentials, update in Render Environment

### Can't connect to database

1. Check DB_HOST is correct
2. Check DB_PASSWORD matches exactly
3. Check database is "Live" on Render

**Fix:** Wait a minute for DNS, verify credentials

---

## Summary

**Total Steps:**
1. Create account (2 min)
2. Create database (2 min)
3. Create web service (5 min)
4. Add environment variables (5 min)
5. Run migrations (2 min)
6. Test (2 min)

**Total Time: ~20 minutes**

**Result: Your backend is LIVE on Render!**

---

**Created:** May 12, 2026
**Status:** Ready to deploy
