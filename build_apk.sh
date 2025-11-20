#!/bin/bash

echo "========================================"
echo "  Fruit Classifier APK Build Script"
echo "========================================"
echo ""

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed!"
    echo "Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "[1/5] Node.js found: $(node --version)"
echo ""

# Check npm installation
if ! command -v npm &> /dev/null; then
    echo "[ERROR] npm is not installed!"
    exit 1
fi

echo "[2/5] npm found: $(npm --version)"
echo ""

# Check if Bubblewrap is installed
if ! command -v bubblewrap &> /dev/null; then
    echo "[3/5] Installing Bubblewrap CLI..."
    npm install -g @bubblewrap/cli
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install Bubblewrap!"
        exit 1
    fi
else
    echo "[3/5] Bubblewrap already installed"
fi
echo ""

# Create icons
echo "[4/5] Creating app icons..."
python3 create_icons.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to create icons. Please create them manually."
    echo "You need: static/img/icon-192.png and static/img/icon-512.png"
fi
echo ""

echo "[5/5] Setup complete!"
echo ""
echo "========================================"
echo "  NEXT STEPS:"
echo "========================================"
echo ""
echo "1. Deploy your Flask app online (Heroku, Railway, etc.)"
echo "   Your app needs to be accessible via HTTPS"
echo ""
echo "2. Update twa-manifest.json with your domain:"
echo "   - Replace 'your-domain.com' with your actual domain"
echo "   - Update all URLs to point to your deployed app"
echo ""
echo "3. Update .well-known/assetlinks.json with your domain"
echo ""
echo "4. Run: bubblewrap init --manifest=https://YOUR-DOMAIN/static/manifest.json"
echo ""
echo "5. Run: bubblewrap build"
echo ""
echo "6. Your APK will be in the current directory!"
echo ""
echo "========================================"
echo "For detailed instructions, see: APK_BUILD_GUIDE.md"
echo "========================================"
