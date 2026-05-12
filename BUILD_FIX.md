# Build Fix - Requirements.txt and Procfile

## Problem

Render build failed with error:
```
ERROR: Could not open requirements.txt: [Errno 2] No such file or directory
```

## Root Cause

The acked backend folder was missing two critical files:
1. **requirements.txt** - List of Python dependencies
2. **Procfile** - How to start the app on Render

## Solution

### Files Created & Pushed to GitHub

#### 1. requirements.txt
```
Django==5.1.4
djangorestframework==3.16.1
django-cors-headers==4.9.0
python-dotenv==1.2.2
Pillow==12.1.1
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
gunicorn==21.2.0
psycopg2-binary==2.9.11
```

This tells Render what Python packages to install.

#### 2. Procfile
```
web: gunicorn acked.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

This tells Render:
- **web:** How to start the Django app (using gunicorn)
- **release:** Run migrations before starting

#### 3. settings.py (Updated)
Already updated with:
- Environment variable support
- PostgreSQL database config
- Cloudinary integration
- CORS and security settings

## What to Do Now

### Option 1: Let Render Auto-Redeploy

Render watches your GitHub repo. Since you pushed the new files:
1. Go to https://render.com/dashboard
2. Click on **acked-backend** service
3. Go to **Logs** tab
4. Watch the new build start automatically
5. Wait for "Live" status (green)

### Option 2: Manual Redeploy

If auto-redeploy doesn't start:
1. Go to Service Dashboard
2. Click **Settings** tab
3. Click **"Redeploy latest commit"** button
4. Wait for build to complete

## What Happens During Build

When you pushed the files, Render will now:
1. Download requirements.txt
2. Run: `pip install -r requirements.txt`
3. Install all 9 packages
4. Build the app
5. Run Procfile's web command

This should take 2-3 minutes.

## After Build Completes

Once you see **"Live"** status (green):

1. Run migrations (if not automatic):
   - Service Dashboard → Shell tab → Connect
   - Type: `python manage.py migrate`

2. Test the API:
   - Visit: `https://acked-backend.onrender.com/shop/categories/`
   - Should see JSON response

## Files Status

✅ **requirements.txt** - Created and pushed
✅ **Procfile** - Created and pushed
✅ **settings.py** - Updated with Render config
✅ **GitHub** - All changes committed and pushed

## Next Steps

1. **Watch the build:**
   - Render Dashboard → acked-backend → Logs tab
   - Build should start automatically

2. **When it says "Live":**
   - Service is ready!

3. **Run migrations (if needed):**
   - Service Dashboard → Shell tab
   - Type: `python manage.py migrate`

4. **Test API:**
   - Visit: `https://acked-backend.onrender.com/shop/categories/`
   - Should return JSON

## Troubleshooting

### Build Still Fails

Check the error in Logs tab:

**Error: "No module named X"**
- Add the module to requirements.txt
- Push to GitHub
- Render auto-redeploys

**Error: "Command 'gunicorn' not found"**
- Gunicorn is in requirements.txt ✓
- Wait for rebuild

**Error: "Port already in use"**
- Render uses $PORT environment variable
- This is automatically set ✓

### App Shows "Build Successful" but API returns Error

1. Check Logs tab for runtime errors
2. Likely: Environment variables missing
   - Add all 14 in Environment tab
   - Service auto-redeploys
3. Or: Database migrations not run
   - Run: `python manage.py migrate` in Shell tab

## Summary

**Problem Solved:** Created missing requirements.txt and Procfile

**Files Added:**
- requirements.txt (9 dependencies)
- Procfile (startup config)

**Pushed to GitHub:** Yes ✓

**Next:** Watch Render auto-redeploy

**Status:** Ready for Render build!

---

**Created:** May 12, 2026
**Status:** ✅ Files created and pushed
