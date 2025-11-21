import os
import cv2
import numpy as np
import tensorflow as tf
from fruit_validator_new import is_fruit_like_optimized

# Load the TFLite model
print("Loading TFLite model...")
interpreter = tf.lite.Interpreter(model_path='fruit_freshness_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("Model loaded successfully!\n")

def auto_white_balance(img):
    """Apply automatic white balance correction"""
    result = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2RGB)
    return result

def preprocess_image(img_path):
    """Enhanced preprocessing for real camera images"""
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Apply CLAHE for better contrast and brightness handling
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    enhanced = cv2.merge((cl, a, b))
    img = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
    
    # Noise reduction for camera images
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # Sharpen the image
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    
    # Auto white balance
    img = auto_white_balance(img)
    
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
    img = img.astype('float32') / 255.0
    img = np.clip(img, 0.0, 1.0)
    img = np.expand_dims(img, axis=0)
    return img

# Test all images in realimages folder
realimages_folder = 'realimages'
image_files = [f for f in os.listdir(realimages_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Found {len(image_files)} images to test\n")
print("=" * 80)

results = []
for idx, img_file in enumerate(image_files, 1):
    img_path = os.path.join(realimages_folder, img_file)
    print(f"\n[{idx}/{len(image_files)}] Testing: {img_file}")
    print("-" * 80)
    
    try:
        # Step 1: Validate fruit image
        print("  ⏳ Running fruit validation...")
        is_valid, confidence, validation_message = is_fruit_like_optimized(img_path)
        
        if not is_valid:
            print(f"  ❌ VALIDATION FAILED: {validation_message}")
            results.append({
                'file': img_file,
                'status': 'FAILED',
                'reason': validation_message
            })
            continue
        else:
            print(f"  ✅ Validation passed: {validation_message} ({confidence:.1f}% confidence)")
        
        # Step 2: Preprocess and predict
        print("  ⏳ Preprocessing image...")
        img_array = preprocess_image(img_path)
        
        print("  ⏳ Running ML prediction...")
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        freshness_score = float(prediction[0][0])
        
        if freshness_score > 0.5:
            result = "FRESH"
            confidence = freshness_score * 100
        else:
            result = "ROTTEN"
            confidence = (1 - freshness_score) * 100
        
        print(f"  ✅ PREDICTION SUCCESS!")
        print(f"     Result: {result}")
        print(f"     Confidence: {confidence:.2f}%")
        print(f"     Raw Score: {freshness_score:.4f}")
        
        results.append({
            'file': img_file,
            'status': 'SUCCESS',
            'result': result,
            'confidence': confidence,
            'score': freshness_score
        })
        
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        results.append({
            'file': img_file,
            'status': 'ERROR',
            'reason': str(e)
        })

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
failed_count = sum(1 for r in results if r['status'] == 'FAILED')
error_count = sum(1 for r in results if r['status'] == 'ERROR')

print(f"\n📊 Overall Results:")
print(f"   Total Images: {len(results)}")
print(f"   ✅ Success: {success_count}")
print(f"   ❌ Failed Validation: {failed_count}")
print(f"   ⚠️  Errors: {error_count}")

if success_count > 0:
    print(f"\n✅ Successful Predictions:")
    for r in results:
        if r['status'] == 'SUCCESS':
            print(f"   • {r['file']}: {r['result']} ({r['confidence']:.1f}% confidence)")

if failed_count > 0:
    print(f"\n❌ Failed Validations:")
    for r in results:
        if r['status'] == 'FAILED':
            print(f"   • {r['file']}: {r['reason']}")

if error_count > 0:
    print(f"\n⚠️  Errors:")
    for r in results:
        if r['status'] == 'ERROR':
            print(f"   • {r['file']}: {r['reason']}")

print("\n" + "=" * 80)
if success_count == len(results):
    print("🎉 ALL IMAGES PROCESSED SUCCESSFULLY!")
elif success_count > 0:
    print(f"⚠️  {success_count}/{len(results)} images processed successfully")
else:
    print("❌ NO IMAGES PROCESSED SUCCESSFULLY - CHECK ERRORS ABOVE")
print("=" * 80)
