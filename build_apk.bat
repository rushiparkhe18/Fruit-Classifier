@echo off
echo ========================================
echo   Fruit Classifier APK Build Script
echo ========================================
echo.

REM Check Node.js installation
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo [1/5] Node.js found: 
node --version
echo.

REM Check npm installation
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed!
    pause
    exit /b 1
)

echo [2/5] npm found:
npm --version
echo.

REM Check if Bubblewrap is installed
where bubblewrap >nul 2>&1
if %errorlevel% neq 0 (
    echo [3/5] Installing Bubblewrap CLI...
    npm install -g @bubblewrap/cli
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Bubblewrap!
        pause
        exit /b 1
    )
) else (
    echo [3/5] Bubblewrap already installed
)
echo.

REM Create icons
echo [4/5] Creating app icons...
python create_icons.py
if %errorlevel% neq 0 (
    echo [WARNING] Failed to create icons. Please create them manually.
    echo You need: static/img/icon-192.png and static/img/icon-512.png
)
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Deploy your Flask app online (Heroku, Railway, etc.)
echo    Your app needs to be accessible via HTTPS
echo.
echo 2. Update twa-manifest.json with your domain:
echo    - Replace "your-domain.com" with your actual domain
echo    - Update all URLs to point to your deployed app
echo.
echo 3. Update .well-known/assetlinks.json with your domain
echo.
echo 4. Run: bubblewrap init --manifest=https://YOUR-DOMAIN/static/manifest.json
echo.
echo 5. Run: bubblewrap build
echo.
echo 6. Your APK will be in the current directory!
echo.
echo ========================================
echo For detailed instructions, see: APK_BUILD_GUIDE.md
echo ========================================
pause
