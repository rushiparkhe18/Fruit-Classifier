# 🚀 Quick Start - Deploy & Build APK

## Step 1: Create Icons (2 minutes)

```powershell
pip install pillow
python create_icons.py
```

This creates:
- `static/img/icon-192.png`
- `static/img/icon-512.png`
- `static/img/favicon.ico`
- `static/img/screenshot1.png`

---

## Step 2: Deploy to Railway (5 minutes)

### Option A: Railway (Recommended - Easiest)

1. **Sign up**: https://railway.app/
2. **New Project** → **Deploy from GitHub repo**
3. **Connect** your GitHub account (or create repo first)
4. **Select** this repository
5. Railway will auto-deploy!
6. **Copy** your deployment URL (e.g., `https://fruit-classifier-production.up.railway.app`)

### Option B: Heroku

```powershell
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create fruit-classifier-app
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option C: Render

1. Sign up: https://render.com/
2. New Web Service → Connect GitHub
3. Deploy automatically

---

## Step 3: Update Configuration (2 minutes)

**Edit `twa-manifest.json`** - Replace `your-domain.com` with your Railway/Heroku URL:

```json
{
  "packageId": "com.fruitclassifier.app",
  "host": "fruit-classifier-production.up.railway.app",
  "name": "Fruit Freshness Classifier",
  "startUrl": "/",
  "iconUrl": "https://fruit-classifier-production.up.railway.app/static/img/icon-512.png",
  "maskableIconUrl": "https://fruit-classifier-production.up.railway.app/static/img/icon-512.png",
  "webManifestUrl": "https://fruit-classifier-production.up.railway.app/static/manifest.json"
}
```

**Edit `.well-known/assetlinks.json`** - Update domain:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "web",
    "site": "https://fruit-classifier-production.up.railway.app"
  }
}]
```

---

## Step 4: Build APK (5 minutes)

### Method 1: Using PWABuilder (EASIEST - No installation needed)

1. Visit: https://www.pwabuilder.com/
2. Enter your Railway URL
3. Click **Start**
4. Click **Package for Stores** → **Android**
5. **Download APK** ✅

**DONE! Install the APK on your phone!**

---

### Method 2: Using Bubblewrap CLI

```powershell
# Install Node.js from: https://nodejs.org/

# Run setup script
.\build_apk.bat

# Initialize Bubblewrap with your URL
bubblewrap init --manifest=https://YOUR-DOMAIN/static/manifest.json

# Build APK
bubblewrap build
```

APK will be generated: `app-release-signed.apk`

---

## Step 5: Install APK on Phone (2 minutes)

### Transfer APK to your phone:

**Option A: Via USB**
```powershell
# Copy APK file to phone storage
# Or use ADB if installed:
adb install app-release-signed.apk
```

**Option B: Via Email/Cloud**
- Email the APK to yourself
- Download on phone
- Tap to install

**Option C: Via Google Drive**
- Upload APK to Google Drive
- Download on phone
- Install

### Enable installation:
1. Settings → Security → **Allow installation from unknown sources**
2. Tap the APK file
3. Tap **Install**

---

## ✅ What's Included

Your APK now has:
- ✅ **Full ML/AI functionality** - TensorFlow model working
- ✅ **Blockchain verification** - All features preserved
- ✅ **Image upload & analysis**
- ✅ **Offline support** (Service Worker)
- ✅ **Native Android app experience**
- ✅ **Professional icon and splash screen**

---

## 🎯 FASTEST PATH (15 minutes total)

1. **Create icons**: `python create_icons.py` (2 min)
2. **Deploy to Railway**: Connect GitHub repo (5 min)
3. **Use PWABuilder**: https://www.pwabuilder.com/ (5 min)
4. **Install on phone**: Transfer & install APK (3 min)

**Total: 15 minutes to a working Android APK!**

---

## Troubleshooting

### "App not installed" error
- Enable "Unknown sources" in phone settings
- Make sure APK downloaded completely

### App crashes
- Verify your web app URL is accessible
- Check that HTTPS is working
- Test the web app in a browser first

### ML model not working
- Your Flask backend must be running and accessible
- The APK loads your web app from the internet
- All AI processing happens on your server

---

## Need Help?

See **APK_BUILD_GUIDE.md** for detailed instructions and alternative methods.
