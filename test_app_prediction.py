"""
Test the Flask app's prediction endpoint with realimages
"""
import os
import requests
import time

# Test images
realimages_folder = "realimages"
images = [f for f in os.listdir(realimages_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Testing {len(images)} images through Flask app...")
print("="*80)
print("⚠️  IMPORTANT: Make sure Flask app is running on http://localhost:5000")
print("="*80)

# Wait for user to start Flask app
time.sleep(2)

passed = 0
failed = 0

for img in sorted(images)[:3]:  # Test first 3 images only
    img_path = os.path.join(realimages_folder, img)
    
    try:
        with open(img_path, 'rb') as f:
            files = {'file': (img, f, 'image/jpeg')}
            response = requests.post('http://localhost:5000/predict', files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            status = "✓ PASS"
            passed += 1
            print(f"{status} | {img:30s} | {data['freshness_level']:12s} | {data['confidence']:.1f}%")
        else:
            status = "✗ FAIL"
            failed += 1
            error_msg = response.json().get('error', 'Unknown error')
            print(f"{status} | {img:30s} | Error: {error_msg}")
    
    except requests.exceptions.ConnectionError:
        print(f"✗ ERROR | Flask app not running! Start with: python app.py")
        break
    except Exception as e:
        status = "✗ FAIL"
        failed += 1
        print(f"{status} | {img:30s} | Exception: {str(e)}")

print("="*80)
print(f"Results: {passed} passed, {failed} failed out of {min(3, len(images))} images tested")
print("\nNote: This test only tests 3 images. Run Flask app manually to test all images.")
