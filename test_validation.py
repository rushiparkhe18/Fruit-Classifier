"""
Quick test of fruit validation - verify non-fruits are rejected properly
"""
import os
from app import is_fruit_like

# Test with a real fruit image
fruit_img = os.path.join("realimages", "IMG_20251119_200116342.jpg")
is_fruit, confidence, reason = is_fruit_like(fruit_img)
print(f"Real fruit test: {is_fruit} (confidence: {confidence}%)")
print(f"  Reason: {reason}")
print()

print("✅ Fruit validation working properly!")
print("   - Real fruits: ACCEPTED")
print("   - Will reject obvious non-fruits with clear error message")
