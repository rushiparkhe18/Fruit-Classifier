"""
Quick Setup: Organize existing images into training structure
"""
import os
import shutil

print("🗂️  Setting up training data structure...")

# Create folders
base_dir = "training_data"
categories = ['fresh', 'slightly_ripe', 'ripe', 'overripe', 'rotten']

for category in categories:
    os.makedirs(os.path.join(base_dir, category), exist_ok=True)

# Map existing images
image_mapping = {
    'fresh': ['apple.jpg', 'mango.jpeg', 'orange.jpeg'],
    'ripe': ['banana.jpeg'],
    'rotten': ['rotrten bana.jpeg', 'rotten apple.jpeg', 'rotten mango.jpg', 'Rotten orange.jpeg']
}

# Copy images
for category, files in image_mapping.items():
    for filename in files:
        src = os.path.join('img', filename)
        dst = os.path.join(base_dir, category, filename)
        
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"  ✅ {filename} → {category}/")

# Copy realimages to fresh
realimages_dir = "realimages"
if os.path.exists(realimages_dir):
    for filename in os.listdir(realimages_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            src = os.path.join(realimages_dir, filename)
            dst = os.path.join(base_dir, 'fresh', f"real_{filename}")
            shutil.copy(src, dst)
            print(f"  ✅ {filename} → fresh/")

print(f"\n✅ Training data ready in '{base_dir}/' folder")
print("\nNext step: python train_simple.py")
