# 🚀 Deployment Quick Reference

## 📋 Start Commands by Platform

### Render:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Railway:
```bash
# Auto-detected from Procfile
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Heroku:
```bash
# Uses Procfile automatically
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

---

## 📦 Build Command (All Platforms):
```bash
pip install -r requirements.txt
```

---

## 🎯 Platform Comparison

| Platform | Setup | Free Tier | Auto Deploy | Best For |
|----------|-------|-----------|-------------|----------|
| **Railway** | Easiest | Yes | Yes | Quick start |
| **Render** | Easy | Yes | Yes | Production |
| **Heroku** | Medium | No* | Yes | Enterprise |

*Heroku discontinued free tier

---

## ⚡ Fastest Deployment (Railway)

1. Visit https://railway.app/
2. Connect GitHub
3. Select repo
4. Deploy (auto-configured)
5. Copy URL

**Time: 2 minutes**

---

## 🔧 Manual Configuration (Render)

1. Visit https://render.com/
2. New Web Service
3. Connect GitHub repo
4. Configure:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Deploy

**Time: 5 minutes**

---

## ✅ Files Already Included

- ✅ `requirements.txt` - Dependencies (with gunicorn)
- ✅ `Procfile` - Heroku/Railway config
- ✅ `render.yaml` - Render auto-config
- ✅ `runtime.txt` - Python version

**Everything is ready to deploy!**

---

## 🧪 Test After Deployment

```bash
# Replace YOUR-URL with your deployment URL

# Test main page
curl https://YOUR-URL/

# Test manifest
curl https://YOUR-URL/static/manifest.json

# Test asset links
curl https://YOUR-URL/.well-known/assetlinks.json
```

---

## 🔄 After Deployment

1. Copy your deployment URL
2. Update `twa-manifest.json` with URL
3. Update `.well-known/assetlinks.json` with URL
4. Generate APK using PWABuilder
5. Done! 🎉

---

## 📚 Full Guides

- **Render**: See `RENDER_DEPLOY.md`
- **Railway/Heroku**: See `DEPLOYMENT_GUIDE.md`
- **APK Build**: See `QUICKSTART_APK.md`

---

**TL;DR**: Use Railway for fastest deployment (2 min), or Render for detailed control (5 min).
