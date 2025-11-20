# 📱 Generate APK for Fruit Freshness Classifier

## ✅ Your Web App is Now PWA-Ready!

Your Flask app has been configured as a Progressive Web App with:
- ✅ Web manifest (`static/manifest.json`)
- ✅ Service Worker for offline support (`static/sw.js`)
- ✅ PWA meta tags in HTML
- ✅ Full ML/AI functionality preserved
- ✅ Blockchain integration working

---

## 🚀 METHOD 1: Using Bubblewrap (EASIEST - 15 minutes)

Bubblewrap is Google's official tool to convert PWAs to Android APKs.

### Prerequisites
1. **Node.js** (v14 or higher): https://nodejs.org/
2. **Java JDK 11+**: https://adoptium.net/
3. **Android SDK**: Will be installed automatically by Bubblewrap

### Step 1: Install Bubblewrap
```powershell
npm install -g @bubblewrap/cli
```

### Step 2: Deploy Your Flask App Online

**IMPORTANT**: Your app must be hosted online with HTTPS. Choose one option:

**Option A: Heroku (Free tier available)**
```powershell
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login and create app
heroku login
heroku create fruit-classifier-app

# Deploy
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

**Option B: Railway.app (Easy deployment)**
1. Go to https://railway.app/
2. Connect your GitHub repository
3. Deploy automatically

**Option C: PythonAnywhere (Simple)**
1. Sign up at https://www.pythonanywhere.com/
2. Upload your files
3. Configure WSGI

**Option D: ngrok (For Testing - Temporary URL)**
```powershell
# Download ngrok: https://ngrok.com/download
# Run your Flask app
python app.py

# In another terminal:
ngrok http 5000
# Copy the https:// URL provided
```

### Step 3: Update TWA Manifest

Edit `twa-manifest.json` and replace:
- `"host": "your-domain.com"` → Your actual domain (e.g., `fruit-classifier-app.herokuapp.com`)
- `"iconUrl"` → Full URL to your icon
- `"maskableIconUrl"` → Full URL to your icon
- `"webManifestUrl"` → Full URL to manifest

Example:
```json
{
  "packageId": "com.fruitclassifier.app",
  "host": "fruit-classifier-app.herokuapp.com",
  "name": "Fruit Freshness Classifier",
  "startUrl": "/",
  "iconUrl": "https://fruit-classifier-app.herokuapp.com/static/img/icon-512.png",
  "webManifestUrl": "https://fruit-classifier-app.herokuapp.com/static/manifest.json"
}
```

### Step 4: Create Icons

You need to create app icons. Create these files:

**Create `static/img/icon-192.png`** (192x192 pixels)
**Create `static/img/icon-512.png`** (512x512 pixels)

Use an online tool like:
- https://www.flaticon.com/ (download fruit icon)
- https://favicon.io/favicon-generator/ (generate icons)
- Or use any image editor to resize a fruit image

### Step 5: Initialize Bubblewrap

```powershell
cd c:\Users\hp\Desktop\fruit-classifier

# Initialize TWA project
bubblewrap init --manifest=https://YOUR-DOMAIN.com/static/manifest.json
```

Follow the prompts and enter:
- App name: `Fruit Freshness Classifier`
- Package ID: `com.fruitclassifier.app`
- Domain: Your deployed domain
- Accept defaults for other options

### Step 6: Build APK

```powershell
# Build the APK
bubblewrap build

# The APK will be created in:
# app-release-signed.apk or app-release-unsigned.apk
```

### Step 7: Install APK on Android

**Transfer to phone:**
```powershell
# If you have ADB (Android Debug Bridge)
adb install app-release-signed.apk

# Or manually:
# - Copy APK to your phone via USB/Email/Cloud
# - Enable "Install from unknown sources" in phone settings
# - Tap the APK file to install
```

---

## 🚀 METHOD 2: PWA Studio (NO CODE - 5 minutes)

### Use PWABuilder (Microsoft's Tool)

1. **Deploy your app online** (see Method 1, Step 2)

2. **Visit**: https://www.pwabuilder.com/

3. **Enter your URL**: https://your-domain.com

4. **Click "Start"** and analyze your PWA

5. **Click "Package for Stores"** → Select "Android"

6. **Download APK** - Ready to install!

---

## 🚀 METHOD 3: Android Studio (ADVANCED - For developers)

### Prerequisites
- Android Studio: https://developer.android.com/studio
- Java JDK 11+

### Step 1: Create New Project

1. Open Android Studio
2. **New Project** → **Empty Activity**
3. Name: `FruitClassifier`
4. Package: `com.fruitclassifier.app`
5. Language: **Kotlin** or **Java**
6. Minimum SDK: **API 24** (Android 7.0)

### Step 2: Add WebView with TWA

**In `app/build.gradle`:**
```gradle
dependencies {
    implementation 'androidx.browser:browser:1.7.0'
    implementation 'com.google.androidbrowserhelper:androidbrowserhelper:2.5.0'
}
```

**In `AndroidManifest.xml`:**
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.fruitclassifier.app">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:icon="@mipmap/ic_launcher"
        android:label="Fruit Classifier"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        
        <activity
            android:name="com.google.androidbrowserhelper.trusted.LauncherActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name="com.google.androidbrowserhelper.trusted.WebViewFallbackActivity"
            android:exported="false" />

        <meta-data
            android:name="android.support.customtabs.trusted.DEFAULT_URL"
            android:value="https://YOUR-DOMAIN.com" />
            
        <meta-data
            android:name="asset_statements"
            android:resource="@string/asset_statements" />
    </application>
</manifest>
```

**In `res/values/strings.xml`:**
```xml
<resources>
    <string name="app_name">Fruit Classifier</string>
    <string name="asset_statements">
        [{
            \"relation\": [\"delegate_permission/common.handle_all_urls\"],
            \"target\": {
                \"namespace\": \"web\",
                \"site\": \"https://YOUR-DOMAIN.com\"
            }
        }]
    </string>
</resources>
```

### Step 3: Build APK

```
Build → Build Bundle(s) / APK(s) → Build APK(s)
```

APK will be in: `app/build/outputs/apk/release/`

---

## 📦 WHAT YOU NEED BEFORE BUILDING

### 1. Create Icon Files

Create a simple fruit icon (192x192 and 512x512 PNG):

**Quick method using Python:**
```python
# create_icons.py
from PIL import Image, ImageDraw, ImageFont

def create_icon(size):
    img = Image.new('RGB', (size, size), color='#10b981')
    draw = ImageDraw.draw(img)
    
    # Draw a simple fruit emoji or text
    font_size = size // 2
    draw.text((size//4, size//4), '🍎', fill='white', font_size=font_size)
    
    img.save(f'static/img/icon-{size}.png')

create_icon(192)
create_icon(512)
print("Icons created!")
```

### 2. Host Your Flask App Online

**The APK will load your web app from the internet, so it must be accessible via HTTPS.**

Choose hosting:
- **Heroku**: Free tier, easy setup
- **Railway**: Modern, automatic deploys
- **PythonAnywhere**: Python-focused hosting
- **Render**: Free tier available
- **Google Cloud Run**: Scalable, free tier

---

## 🎯 RECOMMENDED WORKFLOW (Fastest Path to APK)

### Quick Start (20 minutes total):

1. **Create icons** (5 min)
   ```powershell
   # Install Pillow if needed
   pip install pillow
   
   # Create icons with emoji or simple design
   # Or download from flaticon.com
   ```

2. **Deploy to Railway** (5 min)
   - Visit https://railway.app/
   - Sign in with GitHub
   - Create new project → Deploy from GitHub
   - Connect your repository
   - Railway will auto-deploy

3. **Use PWABuilder** (5 min)
   - Visit https://www.pwabuilder.com/
   - Enter your Railway URL
   - Generate Android package
   - Download APK

4. **Install on phone** (5 min)
   - Transfer APK to phone
   - Install and test

---

## 📱 Testing Your APK

### Test on emulator (Android Studio):
1. Open AVD Manager
2. Create virtual device
3. Drag APK onto emulator
4. Test all features

### Test on real device:
1. Enable Developer Options
2. Enable USB Debugging
3. Connect phone via USB
4. `adb install your-app.apk`

---

## 🔧 Troubleshooting

### "App not installed" error:
- Enable "Install from unknown sources"
- Settings → Security → Unknown sources

### App crashes on launch:
- Check if your web app URL is accessible
- Verify HTTPS is working
- Check Android logs: `adb logcat`

### ML model not working:
- Your Flask backend handles all ML processing
- Ensure server is running and accessible
- Check network permissions in manifest

### Camera not working:
- Add camera permissions to AndroidManifest.xml:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" />
```

---

## ✅ Your App Features (All Preserved):
- ✅ AI/ML fruit freshness detection (TensorFlow)
- ✅ Blockchain verification
- ✅ Image upload
- ✅ Real-time analysis
- ✅ History tracking
- ✅ Offline support (via service worker)

---

## 📝 Next Steps

1. **Choose Method 1 (Bubblewrap)** for quickest results
2. **Deploy your app online** (Railway/Heroku)
3. **Create icon files** (use Pillow or online tool)
4. **Update `twa-manifest.json`** with your domain
5. **Run Bubblewrap build**
6. **Install APK on your phone**

Need help with any step? Let me know!
