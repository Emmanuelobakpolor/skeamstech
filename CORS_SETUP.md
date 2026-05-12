# CORS & ALLOWED_HOSTS Setup for Render Backend

## Problem

Your Render backend needs to know:
1. Which frontend URLs are allowed (CORS_ALLOWED_ORIGINS)
2. Which hostnames can access it (ALLOWED_HOSTS)

Without these, your Vercel frontend will get blocked!

---

## Solution: Update 3 Environment Variables

Go to your **Render backend service dashboard** and update these 3 variables:

### Variable 1: ALLOWED_HOSTS

**Key:** `ALLOWED_HOSTS`

**Current Value:**
```
acked-backend.onrender.com,localhost
```

**New Value (after Vercel deployment):**
```
acked-backend.onrender.com,localhost,127.0.0.1
```

**Why:** Tells Django which hostnames can access it

---

### Variable 2: CORS_ALLOWED_ORIGINS

**Key:** `CORS_ALLOWED_ORIGINS`

**Current Value:**
```
http://localhost:3000,http://localhost:3001,https://your-frontend.vercel.app
```

**New Value (when you deploy to Vercel):**
```
http://localhost:3000,http://localhost:3001,https://skeamstech.vercel.app
```

(Replace `skeamstech.vercel.app` with your actual Vercel URL)

**Why:** Allows your frontend to make API requests to backend

---

### Variable 3: CSRF_TRUSTED_ORIGINS

**Key:** `CSRF_TRUSTED_ORIGINS`

**Current Value:**
```
https://your-frontend.vercel.app
```

**New Value (when you deploy to Vercel):**
```
https://skeamstech.vercel.app
```

(Replace with your actual Vercel URL)

**Why:** Allows your frontend to POST data to backend (forms, etc.)

---

## Step-by-Step: How to Update

### 1. Go to Render Dashboard
```
https://render.com/dashboard
```

### 2. Click on Your Backend Service
```
acked-backend
```

### 3. Go to Environment Tab
```
Click "Environment" in left sidebar
```

### 4. Update CORS_ALLOWED_ORIGINS

1. Find the variable: `CORS_ALLOWED_ORIGINS`
2. Click the edit button (pencil icon)
3. Change the value to:
   ```
   http://localhost:3000,http://localhost:3001,https://skeamstech.vercel.app
   ```
4. Click "Save"

### 5. Update CSRF_TRUSTED_ORIGINS

1. Find the variable: `CSRF_TRUSTED_ORIGINS`
2. Click the edit button
3. Change the value to:
   ```
   https://skeamstech.vercel.app
   ```
4. Click "Save"

### 6. Update ALLOWED_HOSTS (optional)

1. Find the variable: `ALLOWED_HOSTS`
2. Click the edit button
3. Make sure it includes:
   ```
   acked-backend.onrender.com,localhost,127.0.0.1
   ```
4. Click "Save"

### 7. Wait for Redeploy

After each save:
- Render auto-redeploys your backend
- Watch "Logs" tab to see "Deployment complete"
- Takes about 1-2 minutes

---

## Timeline

### Local Development (now)
```
ALLOWED_HOSTS = localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = http://localhost:3000,http://localhost:3001
```

### After Vercel Deployment
```
ALLOWED_HOSTS = acked-backend.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = http://localhost:3000,http://localhost:3001,https://skeamstech.vercel.app
CSRF_TRUSTED_ORIGINS = https://skeamstech.vercel.app
```

---

## Your Final Configuration

### Render Backend (Django)

```
ALLOWED_HOSTS = acked-backend.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS = http://localhost:3000,http://localhost:3001,https://skeamstech.vercel.app
CSRF_TRUSTED_ORIGINS = https://skeamstech.vercel.app
```

### Vercel Frontend (Next.js)

```
NEXT_PUBLIC_API_URL = https://acked-backend.onrender.com
```

---

## What Each Setting Does

### ALLOWED_HOSTS
- **Django security setting**
- Prevents Host header attacks
- Only hostnames listed can access the app
- Include: backend domain + localhost for testing

### CORS_ALLOWED_ORIGINS
- **Cross-Origin Resource Sharing**
- Allows frontend to make API requests
- Without this: browser blocks requests (CORS error)
- Include: frontend URLs (localhost + Vercel)

### CSRF_TRUSTED_ORIGINS
- **Cross-Site Request Forgery protection**
- Allows forms and POST requests from frontend
- Without this: POST requests get 403 Forbidden
- Include: production frontend URL

---

## Common CORS Errors (Fixed by This)

### Error: "Access to XMLHttpRequest blocked by CORS policy"

**Cause:** Frontend URL not in CORS_ALLOWED_ORIGINS

**Solution:** Add your Vercel URL to CORS_ALLOWED_ORIGINS

**Before:**
```
CORS_ALLOWED_ORIGINS = http://localhost:3000
```

**After:**
```
CORS_ALLOWED_ORIGINS = http://localhost:3000,https://skeamstech.vercel.app
```

---

### Error: "403 Forbidden" on POST requests

**Cause:** Frontend URL not in CSRF_TRUSTED_ORIGINS

**Solution:** Add your Vercel URL to CSRF_TRUSTED_ORIGINS

**Before:**
```
CSRF_TRUSTED_ORIGINS = https://example.com
```

**After:**
```
CSRF_TRUSTED_ORIGINS = https://skeamstech.vercel.app
```

---

### Error: "Bad Request (400)" or "Host not allowed"

**Cause:** Vercel URL not in ALLOWED_HOSTS

**Solution:** Add your Vercel URL to ALLOWED_HOSTS

**Before:**
```
ALLOWED_HOSTS = localhost,127.0.0.1
```

**After:**
```
ALLOWED_HOSTS = acked-backend.onrender.com,localhost,127.0.0.1
```

---

## Testing After Update

### Test CORS

Open browser DevTools (F12) and run in console:

```javascript
fetch('https://acked-backend.onrender.com/shop/categories/')
  .then(res => res.json())
  .then(data => console.log('Success:', data))
  .catch(err => console.log('Error:', err))
```

Should work without CORS errors!

### Test from Frontend

In your Next.js/React app:

```javascript
const API_URL = 'https://acked-backend.onrender.com';

fetch(`${API_URL}/shop/categories/`)
  .then(res => res.json())
  .then(data => console.log(data))
```

Should return categories!

---

## Checklist

- [ ] Vercel frontend is deployed (https://skeamstech.vercel.app)
- [ ] Copied Vercel URL
- [ ] Updated CORS_ALLOWED_ORIGINS with Vercel URL
- [ ] Updated CSRF_TRUSTED_ORIGINS with Vercel URL
- [ ] Updated ALLOWED_HOSTS if needed
- [ ] Render backend redeployed (watched Logs tab)
- [ ] Tested API call from Vercel frontend
- [ ] No CORS errors in browser console
- [ ] API data displays correctly

---

## Summary

**3 Variables to Update on Render:**

1. `ALLOWED_HOSTS` - Add your Vercel URL + render domain
2. `CORS_ALLOWED_ORIGINS` - Add your Vercel URL + localhost
3. `CSRF_TRUSTED_ORIGINS` - Add your Vercel URL

**After Update:**
- Render auto-redeploys
- Wait 1-2 minutes
- Test from your Vercel frontend
- Should work!

---

**Created:** May 12, 2026
**Status:** Ready to configure
