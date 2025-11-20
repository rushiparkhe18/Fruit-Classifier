# 🚀 Render Deployment Guide

## Quick Deploy to Render

Render is a modern cloud platform that makes deployment easy!

---

## 📋 Prerequisites

- GitHub account
- Your code pushed to GitHub repository

---

## 🚀 Method 1: Using render.yaml (Automatic)

Your project already has `render.yaml` configured!

### Steps:

1. **Sign up** at https://render.com/

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `Fruit-Classifier`

3. **Render will auto-detect** the `render.yaml` file and configure everything!

4. **Click "Create Web Service"**

5. **Wait for deployment** (5-10 minutes first time)

6. **Copy your URL**: `https://fruit-classifier.onrender.com`

---

## 🚀 Method 2: Manual Configuration

If you prefer manual setup:

### Steps:

1. **Sign up** at https://render.com/

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub → Select repository

3. **Configure**:
   ```
   Name: fruit-classifier
   Region: Oregon (or closest to you)
   Branch: main
   Runtime: Python 3
   ```

4. **Build Command**:
   ```
   pip install -r requirements.txt
   ```

5. **Start Command**:
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

6. **Plan**: Free

7. **Environment Variables** (optional):
   - `PYTHON_VERSION` = `3.11.0`

8. **Click "Create Web Service"**

---

## ✅ What Happens Next

1. **Render clones your repo**
2. **Installs dependencies** from requirements.txt
3. **Runs the start command** (gunicorn)
4. **Assigns a URL**: `https://your-app.onrender.com`
5. **App is live!** 🎉

---

## 📝 Important Notes

### Free Tier Limitations:
- ⚠️ **Spins down after 15 min of inactivity**
- ⚠️ **First request may take 30-60 seconds** (cold start)
- ✅ **750 hours/month free**
- ✅ **Automatic HTTPS**
- ✅ **Automatic deploys** on git push

### For Production:
- Upgrade to paid plan ($7/month) for:
  - No spin-down
  - Instant response
  - More resources

---

## 🔧 Configuration Files

Your project includes:

### `render.yaml`:
```yaml
services:
  - type: web
    name: fruit-classifier
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

### `Procfile` (backup):
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### `requirements.txt`:
Includes all dependencies including `gunicorn`

---

## 🧪 Testing Your Deployment

After deployment completes:

### 1. Test Main Page:
```
https://your-app.onrender.com/
```
Should load the fruit classifier interface

### 2. Test Manifest:
```
https://your-app.onrender.com/static/manifest.json
```
Should return JSON

### 3. Test Asset Links:
```
https://your-app.onrender.com/.well-known/assetlinks.json
```
Should return JSON

### 4. Test Upload:
- Open your app URL
- Try uploading a fruit image
- Verify ML prediction works
- Check blockchain verification

---

## 🔄 Updating Your App

### Automatic Deploys:

1. Make changes to your code
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Render auto-deploys! ✅
4. Check deployment logs in Render dashboard

---

## 📊 Monitoring

### View Logs:
1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs

### Check Status:
- Dashboard shows service status
- Green = Running
- Yellow = Deploying
- Red = Failed

---

## 🐛 Troubleshooting

### Build Fails:
- Check logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python version compatibility

### App Won't Start:
- Check start command is correct
- Verify `gunicorn` is in requirements.txt
- Check port binding (should use `$PORT`)

### ML Model Not Working:
- Ensure `fruit_freshness_model.h5` is in repo
- Check file size (Render free tier: 512MB limit)
- Verify TensorFlow is installed

### 502 Bad Gateway:
- App may be spinning down (free tier)
- Wait 30-60 seconds and refresh
- Consider upgrading to paid plan

---

## 💡 Tips for Better Performance

### 1. Reduce Cold Starts:
```python
# Add health check endpoint in app.py
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

### 2. Keep App Warm (optional):
- Use UptimeRobot to ping every 5 minutes
- Free service: https://uptimerobot.com/

### 3. Optimize Model Loading:
- Model loads on startup (already done)
- Use smaller model if possible

---

## 🔐 Security

Render provides:
- ✅ Automatic HTTPS/SSL
- ✅ DDoS protection
- ✅ Private environment variables
- ✅ No exposed credentials

---

## 📱 After Deployment - Build APK

Once deployed:

1. **Copy your Render URL**: `https://fruit-classifier.onrender.com`

2. **Update `twa-manifest.json`**:
   ```json
   {
     "host": "fruit-classifier.onrender.com",
     "iconUrl": "https://fruit-classifier.onrender.com/static/img/icon-512.png",
     "webManifestUrl": "https://fruit-classifier.onrender.com/static/manifest.json"
   }
   ```

3. **Update `.well-known/assetlinks.json`**:
   ```json
   [{
     "target": {
       "site": "https://fruit-classifier.onrender.com"
     }
   }]
   ```

4. **Follow APK build instructions** in `QUICKSTART_APK.md`

---

## 💰 Pricing

### Free Tier:
- 750 hours/month
- 512 MB RAM
- Automatic HTTPS
- Spins down after inactivity

### Starter ($7/month):
- Always on (no spin down)
- 512 MB RAM
- Faster response times

### Standard ($25/month):
- 2 GB RAM
- Better for ML models
- Production-ready

---

## 🎯 Quick Start Checklist

- [ ] Sign up at Render.com
- [ ] Connect GitHub account
- [ ] Create new Web Service
- [ ] Select Fruit-Classifier repo
- [ ] Render auto-configures from render.yaml
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (~5-10 min)
- [ ] Copy deployment URL
- [ ] Test URL in browser
- [ ] Update APK config files with URL
- [ ] Generate APK using PWABuilder

---

## 🆚 Render vs Other Platforms

| Feature | Render | Railway | Heroku |
|---------|--------|---------|--------|
| Free Tier | ✅ Yes | ✅ Yes | ❌ No |
| Auto-deploy | ✅ Yes | ✅ Yes | ✅ Yes |
| HTTPS | ✅ Free | ✅ Free | ✅ Free |
| Cold Starts | Yes | No | N/A |
| Setup | Easy | Easiest | Medium |

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Python Guide**: https://render.com/docs/deploy-flask
- **Troubleshooting**: https://render.com/docs/troubleshooting

---

## ✅ Summary

**Start Command for Render**:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**This is already configured in**:
- ✅ `render.yaml` (automatic)
- ✅ `Procfile` (backup)
- ✅ `requirements.txt` (includes gunicorn)

**Just deploy and it works!** 🚀

---

Need help? Check `QUICKSTART_APK.md` for complete deployment workflow!
