"""
Test script to verify PWA configuration
Run this to check if your app is ready for APK generation
"""

import os
import json
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_json_valid(filepath, required_keys=None):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if required_keys:
            missing = [key for key in required_keys if key not in data]
            if missing:
                print(f"  ⚠️  Missing keys: {', '.join(missing)}")
                return False
        
        print(f"  ✅ Valid JSON with all required keys")
        return True
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 PWA & APK Configuration Checker")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check critical files
    print("📁 Checking Critical Files...")
    print("-" * 60)
    
    files_to_check = [
        ('static/manifest.json', 'PWA Manifest'),
        ('static/sw.js', 'Service Worker'),
        ('twa-manifest.json', 'TWA Manifest'),
        ('.well-known/assetlinks.json', 'Asset Links'),
        ('static/img/icon-192.png', 'App Icon 192x192'),
        ('static/img/icon-512.png', 'App Icon 512x512'),
        ('app.py', 'Flask App'),
        ('templates/index.html', 'HTML Template'),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print()
    
    # Check JSON configurations
    print("🔧 Checking JSON Configurations...")
    print("-" * 60)
    
    # Check PWA manifest
    print("Checking static/manifest.json:")
    if os.path.exists('static/manifest.json'):
        manifest_keys = ['name', 'short_name', 'start_url', 'display', 'icons']
        if not check_json_valid('static/manifest.json', manifest_keys):
            all_checks_passed = False
    
    # Check TWA manifest
    print("\nChecking twa-manifest.json:")
    if os.path.exists('twa-manifest.json'):
        twa_keys = ['packageId', 'host', 'name', 'startUrl', 'iconUrl']
        if not check_json_valid('twa-manifest.json', twa_keys):
            all_checks_passed = False
        
        # Check if domain is configured
        with open('twa-manifest.json', 'r', encoding='utf-8') as f:
            twa_data = json.load(f)
        
        if twa_data.get('host') == 'your-domain.com':
            print("  ⚠️  WARNING: Domain not configured! Update 'host' field")
            print("     Replace 'your-domain.com' with your actual deployment URL")
            all_checks_passed = False
    
    # Check asset links
    print("\nChecking .well-known/assetlinks.json:")
    if os.path.exists('.well-known/assetlinks.json'):
        if not check_json_valid('.well-known/assetlinks.json'):
            all_checks_passed = False
        
        # Check if domain is configured
        with open('.well-known/assetlinks.json', 'r', encoding='utf-8') as f:
            asset_data = json.load(f)
        
        if asset_data[0]['target']['site'] == 'https://your-domain.com':
            print("  ⚠️  WARNING: Domain not configured! Update 'site' field")
            all_checks_passed = False
    
    print()
    
    # Check Flask app routes
    print("🌐 Checking Flask Routes...")
    print("-" * 60)
    
    if os.path.exists('app.py'):
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        routes = [
            ('/', 'Main route'),
            ('/predict', 'Prediction route'),
            ('/static/manifest.json', 'Manifest route'),
            ('/.well-known/assetlinks.json', 'Asset links route'),
        ]
        
        for route, description in routes:
            if route in content or f"'{route}'" in content or f'"{route}"' in content:
                print(f"✅ {description}: {route}")
            else:
                print(f"⚠️  {description} not found: {route}")
    
    print()
    
    # Check HTML PWA tags
    print("📄 Checking HTML PWA Tags...")
    print("-" * 60)
    
    if os.path.exists('templates/index.html'):
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        pwa_elements = [
            ('manifest.json', 'Manifest link'),
            ('theme-color', 'Theme color meta tag'),
            ('apple-mobile-web-app-capable', 'Apple PWA meta tag'),
            ('serviceWorker.register', 'Service Worker registration'),
        ]
        
        for element, description in pwa_elements:
            if element in html_content:
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} not found")
                all_checks_passed = False
    
    print()
    
    # Check icon sizes
    print("🎨 Checking Icon Sizes...")
    print("-" * 60)
    
    try:
        from PIL import Image
        
        icons = [
            ('static/img/icon-192.png', 192, 192),
            ('static/img/icon-512.png', 512, 512),
        ]
        
        for filepath, expected_width, expected_height in icons:
            if os.path.exists(filepath):
                img = Image.open(filepath)
                if img.size == (expected_width, expected_height):
                    print(f"✅ {filepath}: {img.size[0]}x{img.size[1]} (Correct)")
                else:
                    print(f"⚠️  {filepath}: {img.size[0]}x{img.size[1]} (Expected: {expected_width}x{expected_height})")
                    all_checks_passed = False
            else:
                print(f"❌ {filepath}: Not found")
                all_checks_passed = False
    except ImportError:
        print("⚠️  Pillow not installed - Cannot verify icon sizes")
        print("   Run: pip install pillow")
    
    print()
    print("=" * 60)
    
    # Final summary
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Your app is ready for APK generation!")
        print()
        print("Next steps:")
        print("1. Deploy your app to Railway/Heroku/Render")
        print("2. Update twa-manifest.json with your deployment URL")
        print("3. Update .well-known/assetlinks.json with your URL")
        print("4. Generate APK using PWABuilder or Bubblewrap")
        print()
        print("See QUICKSTART_APK.md for detailed instructions.")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before generating APK.")
        print("Most issues are warnings and won't prevent APK generation,")
        print("but configuring your domain is required!")
    
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == '__main__':
    sys.exit(main())
