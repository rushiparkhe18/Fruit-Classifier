"""
Test rot detection on real fruit images
"""
import cv2
from app import detect_rotten_features

# Test images from realimages folder
import os

realimages_folder = "realimages"
images = [f for f in os.listdir(realimages_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Testing rot detection on {len(images)} images...")
print("="*80)

for img in sorted(images):
    img_path = os.path.join(realimages_folder, img)
    is_rotten, rot_score, details = detect_rotten_features(img_path)
    
    status = "🔴 ROTTEN" if is_rotten else "✅ FRESH"
    print(f"{status:12s} | {img:30s} | Score: {rot_score:3.0f}/100")
    
    if is_rotten:
        print(f"             | Details: {details}")

print("="*80)
print("Note: Good fresh fruits should show ✅ FRESH with low scores (<100)")
