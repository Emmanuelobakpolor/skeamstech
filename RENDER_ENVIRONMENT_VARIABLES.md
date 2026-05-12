# Render Environment Variables for Acked Backend

## All Environment Variables You Need for Render

When you deploy to Render, you need to add these environment variables in the Render dashboard.

---

## Step-by-Step: Adding Variables to Render

1. **Go to Render Dashboard:** https://render.com/dashboard
2. **Click on your Web Service** (fundspree-backend or acked)
3. **Go to "Environment"** tab (left sidebar)
4. **Click "Add Environment Variable"** for each one below
5. **Copy-paste the Key and Value**

---

## Required Environment Variables

### 1. DJANGO SETTINGS

**Key:** `SECRET_KEY`
**Value:** Generate a new one with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
**Example:**
```
px8$n%j#@k*l&9m^2p5q!r3s4t6u7v8w9x0y1z2a
```

---

**Key:** `DEBUG`
**Value:** 
```
False
```
(Always False for production!)

---

**Key:** `ALLOWED_HOSTS`
**Value:** 
```
acked-backend.onrender.com,localhost
```
(Replace "acked-backend" with your actual Render service name)

---

### 2. DATABASE (PostgreSQL on Render)

**Key:** `DB_ENGINE`
**Value:**
```
django.db.backends.postgresql
```

---

**Key:** `DB_NAME`
**Value:**
```
ackeddb
```
(Or whatever you name your PostgreSQL database)

---

**Key:** `DB_USER`
**Value:**
```
ackeddb_user
```
(Or whatever user you create in PostgreSQL)

---

**Key:** `DB_PASSWORD`
**Value:**
```
your_very_secure_password_here
```
(Generate a strong password and save it!)

---

**Key:** `DB_HOST`
**Value:**
```
dpg-xxxxxxxxxxxxx.render.com
```
(You'll get this from Render PostgreSQL instance)

---

**Key:** `DB_PORT`
**Value:**
```
5432
```

---

### 3. CLOUDINARY (Image Storage)

**Key:** `CLOUDINARY_CLOUD_NAME`
**Value:**
```
your_cloud_name
```
(Get from: https://cloudinary.com/console/settings)

---

**Key:** `CLOUDINARY_API_KEY`
**Value:**
```
123456789012345
```
(Get from Cloudinary dashboard)

---

**Key:** `CLOUDINARY_API_SECRET`
**Value:**
```
abcdefghijklmnopqrstuvwxyz
```
(Get from Cloudinary dashboard - keep it SECRET!)

---

### 4. CORS & Security

**Key:** `CORS_ALLOWED_ORIGINS`
**Value:**
```
http://localhost:3000,http://localhost:3001,https://your-frontend.vercel.app
```
(Multiple URLs separated by comma)

---

**Key:** `CSRF_TRUSTED_ORIGINS`
**Value:**
```
https://your-frontend.vercel.app
```
(Your frontend URL on Vercel)

---

## Complete List (Copy-Paste Ready)

Add all these to Render (14 environment variables):

```
SECRET_KEY = px8$n%j#@k*l&9m^2p5q!r3s4t6u7v8w9x0y1z2a
DEBUG = False
ALLOWED_HOSTS = acked-backend.onrender.com,localhost

DB_ENGINE = django.db.backends.postgresql
DB_NAME = ackeddb
DB_USER = ackeddb_user
DB_PASSWORD = your_secure_password
DB_HOST = dpg-xxxxxxxxxxxxx.render.com
DB_PORT = 5432

CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = 123456789012345
CLOUDINARY_API_SECRET = abcdefghijklmnopqrstuvwxyz

CORS_ALLOWED_ORIGINS = http://localhost:3000,https://your-frontend.vercel.app
CSRF_TRUSTED_ORIGINS = https://your-frontend.vercel.app
```

---

## Where to Get Each Value

### SECRET_KEY
Generate with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### DEBUG
Always set to: `False`

### ALLOWED_HOSTS
Your Render service domain (e.g., `acked-backend.onrender.com`)

### DB_ENGINE
Always: `django.db.backends.postgresql`

### DB_NAME, DB_USER, DB_PASSWORD
You choose these when creating PostgreSQL on Render

### DB_HOST, DB_PORT
Render PostgreSQL will give you these

### CLOUDINARY_CLOUD_NAME, API_KEY, API_SECRET
Get from Cloudinary dashboard:
1. Go to https://cloudinary.com/console/settings
2. Find "API Keys" section
3. Copy Cloud Name, API Key, API Secret

### CORS_ALLOWED_ORIGINS
Your frontend URL (local + production)

### CSRF_TRUSTED_ORIGINS
Your production frontend URL

---

## How Render Shows These

In Render Dashboard:

```
┌─────────────────────────────────────────────┐
│ Environment                                  │
├─────────────────────────────────────────────┤
│ SECRET_KEY          = px8$n%j#@k*l&9m^...   │
│ DEBUG               = False                  │
│ ALLOWED_HOSTS       = acked-backend.o...    │
│ DB_ENGINE           = django.db.backend...  │
│ DB_NAME             = ackeddb               │
│ DB_USER             = ackeddb_user          │
│ DB_PASSWORD         = ••••••••••••••        │
│ DB_HOST             = dpg-xxxxxxxxxxxxx...  │
│ DB_PORT             = 5432                  │
│ CLOUDINARY_CLOUD... = your_cloud_name       │
│ CLOUDINARY_API_KEY  = 123456789012345       │
│ CLOUDINARY_API_SE.. = ••••••••••••••        │
│ CORS_ALLOWED_ORIG.. = http://localhost...   │
│ CSRF_TRUSTED_ORIGI. = https://your-fro...   │
└─────────────────────────────────────────────┘
```

---

## Summary Table

| Variable | Type | Example | Where to Get |
|----------|------|---------|--------------|
| `SECRET_KEY` | String | `px8$n%j#@k*...` | Generate with Python |
| `DEBUG` | Boolean | `False` | Always False! |
| `ALLOWED_HOSTS` | String | `acked-backend.onrender.com` | Your Render domain |
| `DB_ENGINE` | String | `django.db.backends.postgresql` | Fixed value |
| `DB_NAME` | String | `ackeddb` | You choose |
| `DB_USER` | String | `ackeddb_user` | You choose |
| `DB_PASSWORD` | String | `secure_password` | You choose |
| `DB_HOST` | String | `dpg-xxxxx.render.com` | Render PostgreSQL |
| `DB_PORT` | String | `5432` | Render PostgreSQL |
| `CLOUDINARY_CLOUD_NAME` | String | `your_cloud_name` | Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | String | `123456789...` | Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | String | `abcdefgh...` | Cloudinary dashboard |
| `CORS_ALLOWED_ORIGINS` | String | `http://localhost:3000,...` | Your frontend URL |
| `CSRF_TRUSTED_ORIGINS` | String | `https://your-frontend...` | Your frontend URL |

---

## ⚠️ Important Notes

1. **SECRET_KEY** - Keep it secret! Generate a new one for production
2. **DEBUG** - Always set to `False` for production
3. **DB_PASSWORD** - Render will show as •••• for security
4. **CLOUDINARY_API_SECRET** - Render will show as •••• for security
5. **CORS_ALLOWED_ORIGINS** - Multiple URLs separated by comma (no spaces)

---

## Testing Locally

Create a `.env` file in your acked folder:

```env
SECRET_KEY=your-generated-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

For local development:
- `DEBUG=True` (shows errors)
- Uses SQLite database (simpler)
- Cloudinary optional (can test locally)

---

## Summary

Your Render settings.py now reads from these environment variables.

Add all 14 to Render dashboard → Service automatically restarts → Deployment complete!

---

**Created:** May 12, 2026
**Status:** Ready to configure Render
