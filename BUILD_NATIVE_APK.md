# 📱 Build Standalone Native APK

## ✨ What You Get:
- ✅ **100% Offline** - No internet required
- ✅ **Fast** - 2-3 second predictions
- ✅ **Small** - Only 30-40 MB (model compressed from 60MB to 10MB)
- ✅ **Blockchain** - Immutable audit trail included
- ✅ **No Server** - All processing on device

---

## 🚀 Build Options

### Option 1: GitHub Actions (Recommended - Easiest) ⭐

1. **Push code to GitHub** (already done! ✅)
2. **Go to**: https://github.com/rushiparkhe18/Fruit-Classifier/actions
3. **Click**: "Build Android APK" workflow
4. **Click**: "Run workflow" → "Run workflow"
5. **Wait**: ~30-40 minutes for build
6. **Download**: APK from "Artifacts" section

**Benefits:**
- No local setup needed
- Cloud build (free on GitHub)
- Automatic builds on every push

---

### Option 2: Local Build with Docker (Windows)

```powershell
# Pull buildozer Docker image
docker pull kivy/buildozer

# Build APK
docker run --rm -v "${PWD}:/app" kivy/buildozer android debug

# APK will be in: bin/fruitfreshnessai-1.0.0-debug.apk
```

**Time**: ~45-60 minutes first build (downloads dependencies)

---

### Option 3: WSL2 on Windows

```bash
# Install WSL2 with Ubuntu
wsl --install Ubuntu

# Inside WSL2:
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk

# Install buildozer
pip3 install buildozer cython

# Build APK
cd /mnt/c/Users/hp/Desktop/fruit-classifier
buildozer android debug
```

---

## 📦 What's Inside the APK:

- `mobile_app.py` - Kivy native UI (100% Python)
- `fruit_freshness_model.tflite` - Compressed ML model (10MB)
- `blockchain.py` - Lightweight blockchain for audit
- All dependencies bundled (TensorFlow Lite, OpenCV, NumPy)

---

## 🎯 Quick Test Locally (Before Building APK)

```powershell
# Install Kivy
pip install kivy numpy opencv-python tensorflow

# Run the mobile app on PC
python mobile_app.py

# Test the functionality:
# 1. Click "Select Image"
# 2. Choose a fruit image
# 3. Click "Analyze"
# 4. See results instantly!
```

---

## 📲 Install APK on Phone

Once built:

```powershell
# Via USB (ADB)
adb install bin\fruitfreshnessai-1.0.0-debug.apk

# Or manually:
# 1. Copy APK to phone
# 2. Enable "Unknown Sources" in Settings
# 3. Tap APK to install
```

---

## ⚡ Performance Comparison

| Method | Speed | Internet | Model Size | Build Time |
|--------|-------|----------|------------|------------|
| **Native APK** | ⚡⚡⚡⚡ 2-3s | ❌ Not needed | 10 MB | 30-45 min |
| Web APK (Render) | ⚡ 5-8s | ✅ Required | 60 MB | 5 min |

---

## 🔧 Customization

Edit `buildozer.spec` to customize:

```ini
# Change app name
title = Your App Name

# Change package ID
package.name = yourappname
package.domain = com.yourcompany

# Change icon
icon.filename = path/to/your/icon.png

# Add more permissions
android.permissions = CAMERA,READ_EXTERNAL_STORAGE
```

---

## 📝 Notes

- **First build**: Takes 30-60 minutes (downloads Android SDK, NDK, dependencies)
- **Subsequent builds**: 5-10 minutes (cached)
- **APK size**: ~35-45 MB (includes TensorFlow Lite + OpenCV)
- **Android support**: API 24+ (Android 7.0+, covers 98% devices)

---

## 🎉 Recommended: Use GitHub Actions

**Easiest path**:
1. Code is already pushed ✅
2. Workflow is configured ✅
3. Just click "Run workflow" on GitHub
4. Download APK when done

**No local setup needed!** ⚡
