import os
from fruit_validator_new import is_fruit_like_optimized

# Test all images in realimages folder
realimages_folder = "realimages"
images = [f for f in os.listdir(realimages_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Testing {len(images)} images from {realimages_folder}/")
print("="*60)

passed = 0
failed = 0

for img in sorted(images):
    img_path = os.path.join(realimages_folder, img)
    is_fruit, confidence, reason = is_fruit_like_optimized(img_path)
    
    status = "✓ PASS" if is_fruit else "✗ FAIL"
    if is_fruit:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} | {img:30s} | Conf: {confidence:3.0f}% | {reason}")

print("="*60)
print(f"Results: {passed} passed, {failed} failed out of {len(images)} images")
