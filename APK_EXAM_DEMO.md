# 🎯 APK Demo for Exam - Local Speed Solution

## Problem:
- Examiner wants APK demo
- Render is too slow (8-15 seconds)
- Need fast responses like local (2-3 seconds)

## ✅ SOLUTION: Local Server + Ngrok + APK

This lets your APK use your **local machine** = **2-3 second responses!**

---

## 🚀 Step-by-Step Setup (10 minutes):

### Step 1: Download Ngrok (2 minutes)

1. Go to: **https://ngrok.com/download**
2. Download for Windows
3. Extract `ngrok.exe` to your project folder
4. **No sign-up needed for basic use!**

---

### Step 2: Start Your Local Server (30 seconds)

```powershell
# In your project folder
cd C:\Users\hp\Desktop\fruit-classifier
python app.py
```

Keep this terminal running!

---

### Step 3: Start Ngrok (30 seconds)

**Open NEW terminal:**

```powershell
# Navigate to where ngrok.exe is
cd C:\Users\hp\Desktop\fruit-classifier

# Start ngrok
.\ngrok http 5000
```

You'll see something like:
```
Forwarding  https://abc123-xyz.ngrok-free.app -> http://localhost:5000
```

**Copy this URL!** (e.g., `https://abc123-xyz.ngrok-free.app`)

---

### Step 4: Update Your APK URLs (3 minutes)

**Edit `twa-manifest.json`:**
```json
{
  "host": "abc123-xyz.ngrok-free.app",
  "iconUrl": "https://abc123-xyz.ngrok-free.app/static/img/icon-512.png",
  "maskableIconUrl": "https://abc123-xyz.ngrok-free.app/static/img/icon-512.png",
  "webManifestUrl": "https://abc123-xyz.ngrok-free.app/static/manifest.json"
}
```

**Edit `.well-known/assetlinks.json`:**
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "web",
    "site": "https://abc123-xyz.ngrok-free.app"
  }
}]
```

**Replace `abc123-xyz` with YOUR ngrok URL!**

---

### Step 5: Rebuild APK (5 minutes)

1. Go to: **https://www.pwabuilder.com/**
2. Enter your ngrok URL: `https://abc123-xyz.ngrok-free.app`
3. Click **"Start"** → **"Package for Stores"** → **"Android"**
4. Download APK

---

### Step 6: Install on Phone (2 minutes)

```powershell
# Install via USB
adb install app-release-signed.apk

# Or copy APK to phone manually
```

---

### Step 7: Demo to Examiner! 🎉

**Before demo:**
1. Keep `python app.py` running ✅
2. Keep `ngrok` running ✅
3. Phone and laptop on **same WiFi** (optional, but helps)

**During demo:**
1. Open APK on phone
2. Upload fruit image
3. **Get result in 2-3 seconds!** ⚡
4. Show examiner the speed
5. Explain it uses ML model + blockchain

---

## ⚡ Performance:

| Method | Speed | For Exam |
|--------|-------|----------|
| **APK + Ngrok + Local** | ⚡⚡⚡⚡⚡ **2-3s** | ✅ **Perfect!** |
| APK + Render | ⚡⚡ 8-15s | ❌ Too slow |
| Local browser demo | ⚡⚡⚡⚡⚡ 2-3s | ❌ No APK |

---

## 🆘 Alternative: Use Android Emulator

If you don't want to rebuild APK:

### Option 1: BlueStacks (Easiest)
1. Download: https://www.bluestacks.com/
2. Install your existing APK in emulator
3. Emulator can access localhost directly!
4. Change APK URL to: `http://10.0.2.2:5000` (emulator's localhost)

### Option 2: Android Studio Emulator
1. Install Android Studio
2. Create virtual device
3. Install your APK
4. Use `http://10.0.2.2:5000` for localhost access

---

## 🎯 RECOMMENDED FOR EXAM:

### **Use Ngrok Method:**

**Pros:**
- ✅ Real APK on real phone
- ✅ 2-3 second responses (local speed!)
- ✅ Impressive for examiner
- ✅ Shows full project (ML + blockchain + mobile)

**Cons:**
- Takes 10 minutes to set up
- Need to keep laptop running during demo

---

## ⏰ Timeline for Exam Day:

**30 minutes before exam:**
1. Download ngrok (2 min)
2. Start local server (30 sec)
3. Start ngrok (30 sec)
4. Copy ngrok URL
5. Update manifest files (2 min)
6. Rebuild APK on PWABuilder (5 min)
7. Install on phone (2 min)
8. **Test once!** (1 min)

**During exam:**
1. Keep laptop running with `python app.py` and `ngrok`
2. Demo APK on phone
3. **2-3 second responses!** 🚀

---

## 🚨 Emergency Backup:

If ngrok doesn't work:

**Plan B: Emulator with existing APK**
1. Use BlueStacks
2. Install your current Render APK
3. Demo on laptop screen
4. Say: "This is the mobile version running on emulator"

**Plan C: Show web version on laptop**
1. Open localhost:5000 in mobile view (F12 → mobile icon)
2. Demo the interface
3. Explain APK works the same way

---

## ✅ Quick Command Cheat Sheet:

```powershell
# Terminal 1: Start Flask
python app.py

# Terminal 2: Start Ngrok (NEW terminal)
.\ngrok http 5000

# Copy the https URL from ngrok
# Update twa-manifest.json and assetlinks.json
# Rebuild APK on pwabuilder.com
# Install on phone: adb install app.apk

# Demo with 2-3 second responses! 🎉
```

---

**This is your best option for impressing examiner with FAST APK demo!** ⚡
