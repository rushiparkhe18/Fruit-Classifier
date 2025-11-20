# ✅ APK Generation Checklist

Use this checklist to track your progress in generating the Android APK.

---

## Phase 1: Preparation ✅ (COMPLETED)

- [x] Project analyzed and requirements understood
- [x] PWA manifest created (`static/manifest.json`)
- [x] Service Worker configured (`static/sw.js`)
- [x] TWA manifest created (`twa-manifest.json`)
- [x] Digital Asset Links created (`.well-known/assetlinks.json`)
- [x] App icons generated (192x192 and 512x512)
- [x] Flask routes updated for manifest and asset links
- [x] HTML updated with PWA meta tags
- [x] Build scripts created (`.bat` and `.sh`)
- [x] Documentation created

---

## Phase 2: Icon Creation ✅ (COMPLETED)

- [x] Run `python create_icons.py`
- [x] Verify `static/img/icon-192.png` exists
- [x] Verify `static/img/icon-512.png` exists
- [x] Verify `static/img/favicon.ico` exists
- [x] Verify `static/img/screenshot1.png` exists

**Optional**: Replace generated icons with custom designs

---

## Phase 3: Deployment (TO DO)

### Choose Your Platform:

#### Option A: Railway ⭐ (Recommended)
- [ ] Sign up at https://railway.app/
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Wait for automatic deployment
- [ ] Copy deployment URL (e.g., `https://xxx.up.railway.app`)
- [ ] Test URL in browser - app should work
- [ ] Test manifest: `https://xxx.up.railway.app/static/manifest.json`
- [ ] Test asset links: `https://xxx.up.railway.app/.well-known/assetlinks.json`

#### Option B: Heroku
- [ ] Install Heroku CLI
- [ ] Run `heroku login`
- [ ] Run `heroku create fruit-classifier-app`
- [ ] Initialize git: `git init`
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Deploy to Heroku"`
- [ ] Deploy: `git push heroku main`
- [ ] Copy app URL (e.g., `https://fruit-classifier-app.herokuapp.com`)
- [ ] Test URL in browser

#### Option C: Render
- [ ] Sign up at https://render.com/
- [ ] New Web Service → Connect GitHub
- [ ] Configure build and start commands
- [ ] Deploy and copy URL
- [ ] Test URL in browser

---

## Phase 4: Configuration Update (TO DO)

### Update `twa-manifest.json`:
- [ ] Open `twa-manifest.json`
- [ ] Replace `"your-domain.com"` with your deployment URL (without `https://`)
- [ ] Update `"iconUrl"` with full URL: `https://YOUR-DOMAIN/static/img/icon-512.png`
- [ ] Update `"maskableIconUrl"` with full URL
- [ ] Update `"webManifestUrl"` with full URL: `https://YOUR-DOMAIN/static/manifest.json`
- [ ] Save file

### Update `.well-known/assetlinks.json`:
- [ ] Open `.well-known/assetlinks.json`
- [ ] Replace `"https://your-domain.com"` with your full deployment URL
- [ ] Save file

### Re-deploy (if needed):
- [ ] Commit changes: `git add . && git commit -m "Update URLs"`
- [ ] Push to deployment platform

---

## Phase 5: APK Generation (TO DO)

### Method 1: PWABuilder (Easiest) ⭐

- [ ] Visit https://www.pwabuilder.com/
- [ ] Enter your deployment URL
- [ ] Click "Start" and wait for analysis
- [ ] Review PWA score (should be high)
- [ ] Click "Package for Stores"
- [ ] Select "Android"
- [ ] Download APK package
- [ ] Extract APK from downloaded ZIP
- [ ] APK is ready!

### Method 2: Bubblewrap CLI

- [ ] Install Node.js from https://nodejs.org/
- [ ] Open PowerShell in project directory
- [ ] Run `.\build_apk.bat` to install Bubblewrap
- [ ] Run: `bubblewrap init --manifest=https://YOUR-DOMAIN/static/manifest.json`
- [ ] Answer prompts (use defaults)
- [ ] Run: `bubblewrap build`
- [ ] APK created: `app-release-signed.apk` or `app-release-unsigned.apk`

### Method 3: Android Studio (Advanced)

- [ ] Install Android Studio
- [ ] Follow detailed instructions in `APK_BUILD_GUIDE.md`
- [ ] Build APK using Gradle

---

## Phase 6: Testing (TO DO)

### Pre-Installation Testing:
- [ ] Visit your deployed app in Chrome mobile
- [ ] Test image upload functionality
- [ ] Test ML model predictions
- [ ] Test blockchain verification
- [ ] Check for PWA install prompt
- [ ] Test offline functionality

### Install APK:
- [ ] Transfer APK to Android phone via:
  - [ ] USB cable
  - [ ] Email attachment
  - [ ] Google Drive/Dropbox
  - [ ] ADB: `adb install your-app.apk`
- [ ] Enable "Install from unknown sources" on phone
- [ ] Tap APK file to install
- [ ] Install successful ✓

### Post-Installation Testing:
- [ ] App icon appears on home screen
- [ ] App opens successfully
- [ ] UI looks correct
- [ ] Upload image works
- [ ] Camera access works (if implemented)
- [ ] ML prediction works
- [ ] Results display correctly
- [ ] Blockchain verification works
- [ ] App doesn't crash
- [ ] Performance is acceptable
- [ ] Offline mode works

---

## Phase 7: Distribution (Optional)

### Direct Distribution:
- [ ] Share APK file via email/cloud
- [ ] Provide installation instructions
- [ ] Gather user feedback

### Google Play Store (Advanced):
- [ ] Create Google Play Developer account ($25 one-time fee)
- [ ] Prepare store listing (screenshots, description)
- [ ] Sign APK with release key
- [ ] Upload to Play Console
- [ ] Submit for review
- [ ] Publish app

---

## Troubleshooting Checklist

If something doesn't work, check:

### Deployment Issues:
- [ ] Web app accessible via HTTPS
- [ ] All endpoints working (`/`, `/predict`, `/blockchain`)
- [ ] Manifest accessible: `/static/manifest.json`
- [ ] Asset links accessible: `/.well-known/assetlinks.json`
- [ ] Icons accessible: `/static/img/icon-512.png`

### APK Issues:
- [ ] Phone has "Unknown sources" enabled
- [ ] APK downloaded completely (not corrupted)
- [ ] Correct Android version (API 21+)
- [ ] Sufficient storage on phone

### App Issues:
- [ ] Check if web app URL in APK is correct
- [ ] Verify HTTPS certificate is valid
- [ ] Check Android logs: `adb logcat`
- [ ] Test web app directly in mobile browser first

---

## Quick Reference

### Important Files:
- `APK_README.md` - Overview and summary
- `QUICKSTART_APK.md` - Fast track guide (15 min)
- `APK_BUILD_GUIDE.md` - Comprehensive instructions
- `DEPLOYMENT_GUIDE.md` - Deployment help
- `twa-manifest.json` - APK configuration
- `static/manifest.json` - PWA configuration

### Important URLs to Test:
- `https://YOUR-DOMAIN/` - Main app
- `https://YOUR-DOMAIN/static/manifest.json` - PWA manifest
- `https://YOUR-DOMAIN/.well-known/assetlinks.json` - Asset links
- `https://YOUR-DOMAIN/static/img/icon-512.png` - App icon

### Quick Commands:
```powershell
# Create icons
python create_icons.py

# Setup Bubblewrap
.\build_apk.bat

# Initialize TWA
bubblewrap init --manifest=https://YOUR-DOMAIN/static/manifest.json

# Build APK
bubblewrap build

# Install on device
adb install app-release-signed.apk
```

---

## Status Summary

- ✅ **Phase 1**: Preparation - COMPLETE
- ✅ **Phase 2**: Icons - COMPLETE
- ⏳ **Phase 3**: Deployment - PENDING (Next step!)
- ⏳ **Phase 4**: Configuration - PENDING
- ⏳ **Phase 5**: APK Generation - PENDING
- ⏳ **Phase 6**: Testing - PENDING
- ⏳ **Phase 7**: Distribution - OPTIONAL

---

## Next Action

**START HERE**: Follow `QUICKSTART_APK.md` for the fastest path!

1. Deploy to Railway (5 minutes)
2. Update configurations (2 minutes)
3. Use PWABuilder to generate APK (5 minutes)
4. Install on phone (3 minutes)

**Total time: 15 minutes to your Android app!**

---

## Notes

- Keep this checklist updated as you progress
- Mark items complete with [x]
- Add notes for any issues encountered
- Share feedback for improvements

Good luck! 🚀
