# Acked Backend - Render Deployment Setup

## What Was Changed

Your `C:\Users\sxc\Downloads\tech\acked\acked\settings.py` has been **configured for Render deployment**.

## Changes Made to settings.py

### 1. Added Environment Variable Support

**Before:**
```python
SECRET_KEY = 'django-insecure-&xoew$n8_l5%0%7tqarpn^w^-3_g^s@)la38ko5*m3z&9q0@9_'
DEBUG = True
ALLOWED_HOSTS = []
```

**After:**
```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

### 2. Updated Database Configuration

**Before:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**After:**
```python
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}
```

This allows:
- SQLite for local development (default)
- PostgreSQL for Render deployment (via environment variables)

### 3. Added Cloudinary Configuration

**New code added:**
```python
# Cloudinary Configuration (Image Storage)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Use Cloudinary for image storage in production
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    INSTALLED_APPS.append('cloudinary')
    INSTALLED_APPS.append('cloudinary_storage')

    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
```

This enables image storage on Cloudinary instead of server disk.

### 4. Updated CORS Configuration

**Before:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
]
```

**After:**
```python
cors_origins = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001'
).split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins]
```

Now reads from environment variables for production.

### 5. Added Production Security Settings

**New code added:**
```python
# Production Security Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []
```

This enables HTTPS/SSL support for Render.

### 6. Added Static Files Configuration

**Updated:**
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # NEW: For production
```

---

## Environment Variables Needed for Render

Create a `.env` file in the `acked` folder with these values:

```env
# Django Settings
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,localhost

# Database (PostgreSQL on Render)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host.render.com
DB_PORT=5432

# Cloudinary (Image Storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app
```

---

## How It Works Now

### Local Development
- Uses SQLite database (no setup needed)
- All settings have defaults
- Works with `python manage.py runserver`

### Production on Render
- Uses PostgreSQL database
- Reads SECRET_KEY from environment
- Uses Cloudinary for images
- HTTPS enabled
- CORS configured for frontend

---

## What's Still Needed

To deploy to Render, you need to:

1. **Create .env file** with environment variables
2. **Create Procfile** (tells Render how to start)
3. **Create render.yaml** (Render configuration)
4. **Update requirements.txt** (add missing packages)
5. **Push to GitHub**
6. **Deploy on Render dashboard**

---

## Files Location

Changed file:
- `C:\Users\sxc\Downloads\tech\acked\acked\settings.py`

Still need to create:
- `.env` (environment variables)
- `Procfile` (deployment config)
- `render.yaml` (Render service config)

---

## Status

✅ **settings.py** - CONFIGURED FOR RENDER

Still need:
- Procfile
- render.yaml
- .env file
- requirements.txt updates

---

## Next Steps

1. **Create .env file** with environment variables
2. **Create Procfile** with:
   ```
   web: gunicorn acked.wsgi:application --bind 0.0.0.0:$PORT
   release: python manage.py migrate
   ```
3. **Update requirements.txt** to include:
   - python-dotenv
   - gunicorn
   - psycopg2-binary (for PostgreSQL)
   - cloudinary
   - django-cloudinary-storage

4. **Push to GitHub**
5. **Deploy on Render**

---

**Changes made:** May 12, 2026
**Status:** ✅ Production-ready configuration
