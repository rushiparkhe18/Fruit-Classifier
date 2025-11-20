"""
Convert TensorFlow model to TensorFlow Lite for smaller APK size
Reduces model from 60MB to ~15-30MB
"""

import tensorflow as tf
import os

print("🔄 Converting model to TensorFlow Lite...")
print("-" * 50)

# Load the original model
print("📂 Loading fruit_freshness_model.h5...")
model = tf.keras.models.load_model('fruit_freshness_model.h5')
print(f"✅ Model loaded successfully")

# Get original model size
original_size = os.path.getsize('fruit_freshness_model.h5') / (1024 * 1024)
print(f"📊 Original model size: {original_size:.2f} MB")

# Convert to TensorFlow Lite with optimizations
print("\n🔧 Converting to TFLite with optimization...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Apply optimizations
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]  # Use float16 for smaller size

# Convert
tflite_model = converter.convert()

# Save the TFLite model
output_file = 'fruit_freshness_model.tflite'
with open(output_file, 'wb') as f:
    f.write(tflite_model)

# Get new size
new_size = os.path.getsize(output_file) / (1024 * 1024)
reduction = ((original_size - new_size) / original_size) * 100

print(f"\n✅ Conversion complete!")
print(f"📊 New model size: {new_size:.2f} MB")
print(f"💾 Size reduced by: {reduction:.1f}%")
print(f"📁 Saved as: {output_file}")

print("\n" + "=" * 50)
print("🎉 Ready for mobile deployment!")
print("=" * 50)
print("\nNext steps:")
print("1. Update main.py to use .tflite model")
print("2. Build APK with buildozer")
print("3. APK will be much smaller and faster!")
