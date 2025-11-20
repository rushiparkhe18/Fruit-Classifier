from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
import os
import hashlib
from datetime import datetime
from blockchain import Blockchain  # Import blockchain module

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

blockchain = Blockchain()

# Load the trained model
model = None
try:
    model = tf.keras.models.load_model('fruit_freshness_model.h5')
    print("Model loaded successfully!")
except:
    print("Model not found. Please train the model first by running train_model.py")

FRESHNESS_LEVELS = [
    'Fresh',
    'Slightly Ripe', 
    'Ripe',
    'Overripe',
    'Rotten'
]

FRESHNESS_INFO = {
    'Fresh': {
        'emoji': '✨',
        'color': '#10b981',
        'description': 'Perfect condition! Best time to consume.',
        'recommendation': 'Enjoy now or store properly for later use.'
    },
    'Slightly Ripe': {
        'emoji': '🌟',
        'color': '#84cc16',
        'description': 'Good condition with optimal ripeness.',
        'recommendation': 'Great for eating! Consume within 2-3 days.'
    },
    'Ripe': {
        'emoji': '⚠️',
        'color': '#f59e0b',
        'description': 'Fully ripe. Should be consumed soon.',
        'recommendation': 'Eat within 1-2 days or use in cooking.'
    },
    'Overripe': {
        'emoji': '⏰',
        'color': '#f97316',
        'description': 'Past peak freshness. Quality declining.',
        'recommendation': 'Use immediately in smoothies or baking.'
    },
    'Rotten': {
        'emoji': '❌',
        'color': '#ef4444',
        'description': 'Spoiled. Not safe for consumption.',
        'recommendation': 'Discard immediately. Do not consume.'
    }
}

def preprocess_image(image_path):
    """
    Preprocess image using OpenCV
    - Read image
    - Resize to model input size
    - Normalize pixel values
    """
    # Read image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert BGR to RGB (OpenCV reads in BGR format)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize image to 128x128 (model input size)
    img_resized = cv2.resize(img, (128, 128))
    
    # Normalize pixel values to [0, 1]
    img_normalized = img_resized.astype('float32') / 255.0
    
    # Add batch dimension
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    return img_batch

def calculate_image_hash(image_path):
    """Calculate SHA-256 hash of the image file"""
    with open(image_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def detect_rotten_features(image_path):
    """
    Advanced rotten detection based on visual features
    Returns: (is_rotten: bool, rot_score: float, details: dict)
    """
    img = cv2.imread(image_path)
    if img is None:
        return False, 0, {}
    
    h, w = img.shape[:2]
    
    # FOCUS ON CENTER REGION (70% of image) to avoid background noise
    center_h_start = int(h * 0.15)
    center_h_end = int(h * 0.85)
    center_w_start = int(w * 0.15)
    center_w_end = int(w * 0.85)
    
    img_center = img[center_h_start:center_h_end, center_w_start:center_w_end]
    
    img_hsv = cv2.cvtColor(img_center, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img_center, cv2.COLOR_BGR2GRAY)
    
    total_pixels = img_center.shape[0] * img_center.shape[1]
    
    h_channel = img_hsv[:, :, 0]
    s_channel = img_hsv[:, :, 1]
    v_channel = img_hsv[:, :, 2]
    
    b_channel = img_center[:, :, 0]
    g_channel = img_center[:, :, 1]
    r_channel = img_center[:, :, 2]
    
    rot_indicators = {}
    rot_score = 0
    
    # PRE-CHECK: Verify there's actual fruit color (not just dark background)
    fruit_color_pixels = np.sum(
        (((h_channel <= 10) | (h_channel >= 160)) & (s_channel >= 40) & (v_channel >= 50)) |  # Red
        ((h_channel >= 5) & (h_channel <= 35) & (s_channel >= 40) & (v_channel >= 50)) |  # Orange/Yellow
        ((h_channel >= 35) & (h_channel <= 90) & (s_channel >= 40) & (v_channel >= 50))  # Green
    )
    fruit_color_ratio = fruit_color_pixels / total_pixels
    rot_indicators['fruit_color_ratio'] = fruit_color_ratio * 100
    
    # Check overall image quality
    avg_brightness_check = np.mean(v_channel)
    
    # Strong penalties for poor quality images
    if fruit_color_ratio < 0.15 or avg_brightness_check < 80:
        rot_indicators['warning'] = 'Poor image quality or insufficient fruit visible'
        # These are likely bad images, not rotten fruit - return NOT rotten
        return False, 0, rot_indicators
    elif fruit_color_ratio < 0.25:
        rot_indicators['warning'] = 'Some background detected'
        background_penalty = True
    else:
        background_penalty = False
    
    # 1. DARK SPOTS - Multiple thresholds for better detection
    very_dark = np.sum((b_channel < 50) & (g_channel < 50) & (r_channel < 50))
    dark = np.sum((b_channel < 80) & (g_channel < 80) & (r_channel < 80))
    
    very_dark_ratio = very_dark / total_pixels
    dark_ratio = dark / total_pixels
    
    rot_indicators['very_dark_spots'] = very_dark_ratio * 100
    rot_indicators['dark_spots'] = dark_ratio * 100
    
    if very_dark_ratio > 0.05:  # 5%+ very dark = strong rot
        rot_score += 40
    elif dark_ratio > 0.08:  # 8%+ dark = moderate rot
        rot_score += 30
    elif dark_ratio > 0.03:  # 3%+ dark = early rot
        rot_score += 20
    
    # 2. BROWN/MUDDY COLORS - Multiple brown ranges
    # Dark brown (deep rot)
    dark_brown = np.sum(
        (h_channel >= 5) & (h_channel <= 25) &
        (s_channel >= 30) & (s_channel <= 255) &
        (v_channel >= 15) & (v_channel <= 100)
    )
    # Medium brown (rotting)
    med_brown = np.sum(
        (h_channel >= 5) & (h_channel <= 30) &
        (s_channel >= 25) & (s_channel <= 180) &
        (v_channel >= 80) & (v_channel <= 150)
    )
    
    brown_ratio = (dark_brown + med_brown) / total_pixels
    rot_indicators['brown_areas'] = brown_ratio * 100
    
    if brown_ratio > 0.12:
        rot_score += 35
    elif brown_ratio > 0.06:
        rot_score += 25
    elif brown_ratio > 0.03:
        rot_score += 15
    
    # 3. WRINKLED/SHRIVELED TEXTURE
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    texture_variance = np.var(laplacian)
    rot_indicators['texture_variance'] = texture_variance
    
    if texture_variance > 1500:  # Very rough = rot
        rot_score += 20
    
    # 4. LOW OVERALL BRIGHTNESS (rotting darkens fruit)
    avg_brightness = np.mean(v_channel)
    rot_indicators['avg_brightness'] = avg_brightness
    
    if avg_brightness < 80:
        rot_score += 25
    elif avg_brightness < 120:
        rot_score += 15
    
    # 5. MOLD - Grayish discoloration
    mold_pixels = np.sum(
        (s_channel < 60) &  # Low saturation (gray)
        (v_channel > 60) & (v_channel < 200)
    )
    mold_ratio = mold_pixels / total_pixels
    rot_indicators['mold_areas'] = mold_ratio * 100
    
    if mold_ratio > 0.25:
        rot_score += 25
    elif mold_ratio > 0.15:
        rot_score += 15
    
    # 6. BRIGHTNESS VARIATION (rot creates blotchy patches)
    brightness_std = np.std(v_channel)
    rot_indicators['brightness_std'] = brightness_std
    
    if brightness_std > 70:  # Very uneven = rot patches
        rot_score += 20
    elif brightness_std > 50:
        rot_score += 10
    
    # 7. COLOR DESATURATION (rot dulls colors)
    avg_saturation = np.mean(s_channel)
    rot_indicators['avg_saturation'] = avg_saturation
    
    if avg_saturation < 50:  # Very dull
        rot_score += 15
    elif avg_saturation < 70:  # Somewhat dull
        rot_score += 8
    
    # 8. BROWNISH HUE DOMINANCE
    brown_hue_pixels = np.sum((h_channel >= 8) & (h_channel <= 28))
    brown_hue_ratio = brown_hue_pixels / total_pixels
    rot_indicators['brown_hue_dominance'] = brown_hue_ratio * 100
    
    if brown_hue_ratio > 0.30:  # 30%+ brown hue
        rot_score += 20
    elif brown_hue_ratio > 0.20:
        rot_score += 10
    
    # 9. SPOT DETECTION - Find concentrated dark/brown spots (rot typically starts in patches)
    kernel = np.ones((5,5), np.uint8)
    dark_mask = ((b_channel < 70) & (g_channel < 70) & (r_channel < 70)).astype(np.uint8)
    dark_dilated = cv2.dilate(dark_mask, kernel, iterations=2)
    num_dark_spots = cv2.connectedComponents(dark_dilated)[0] - 1  # -1 for background
    
    rot_indicators['dark_spot_count'] = num_dark_spots
    if num_dark_spots > 5:  # Multiple dark spots = spreading rot
        rot_score += 20
    elif num_dark_spots > 2:
        rot_score += 10
    
    # 10. SOFTNESS INDICATOR - Low contrast = mushy/soft texture
    contrast = np.max(v_channel) - np.min(v_channel)
    rot_indicators['contrast'] = contrast
    if contrast < 100:  # Very low contrast = soft/mushy
        rot_score += 15
    
    # APPLY BACKGROUND PENALTY
    if background_penalty:
        rot_score = int(rot_score * 0.6)  # Reduce score by 40% if too much background
        rot_indicators['background_penalty_applied'] = True
    
    # DECISION: Threshold for rotten classification
    is_rotten = rot_score >= 50
    
    rot_indicators['final_score'] = rot_score
    
    return is_rotten, rot_score, rot_indicators

def is_fruit_like(image_path):
    """
    OPTIMIZED fruit detection - Fast, accurate, handles all cases
    Returns: (is_fruit: bool, confidence: float, reason: str)
    """
    img = cv2.imread(image_path)
    if img is None:
        return False, 0, "Unable to read image"
    
    h, w = img.shape[:2]
    total_pixels = h * w
    
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ===== LAYER 1: HARD REJECTS (Fast elimination) =====
    
    # Check unique colors
    unique_colors = len(np.unique(img.reshape(-1, img.shape[2]), axis=0))
    if unique_colors < 50:
        return False, 0, "Simple graphic"
    
    # Calculate edges FIRST (needed by multiple checks)
    edges = cv2.Canny(gray, 100, 200)
    edge_ratio = np.sum(edges > 0) / total_pixels
    
    # Check for multiple circles (vehicles) - BALANCED sensitivity
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=100, param2=40, minRadius=30, maxRadius=300)
    num_circles = len(circles[0]) if circles is not None else 0
    
    # STRICT vehicle detection: 2+ circles AND high edges
    if num_circles >= 2 and edge_ratio > 0.12:
        return False, 0, "Vehicle detected (multiple wheels)"
    
    # Check for metallic/reflective surfaces (cars, bikes)
    hist_peaks = np.histogram(gray, bins=256)[0]
    has_metallic_peaks = np.max(hist_peaks) > (total_pixels * 0.2)  # Very strong concentration
    if has_metallic_peaks and edge_ratio > 0.20 and num_circles >= 1:
        return False, 0, "Metallic vehicle surface"
    
    # Check for very sharp mechanical edges
    if edge_ratio > 0.30:
        return False, 0, "Mechanical object (too many sharp edges)"
    
    # Check for artificial straight lines (vehicle frames)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)
    num_lines = len(lines) if lines is not None else 0
    if num_lines > 30 and edge_ratio > 0.15:
        return False, 0, "Artificial structure detected"
    
    # ===== LAYER 2: FRUIT COLOR ANALYSIS (Generous ranges) =====
    
    h_channel = img_hsv[:, :, 0]
    s_channel = img_hsv[:, :, 1]
    v_channel = img_hsv[:, :, 2]
    
    # All fruit colors including brown for rotten
    fruit_pixels = (
        # Red
        ((h_channel <= 10) | (h_channel >= 160)) & (s_channel >= 30) & (v_channel >= 30) |
        # Orange  
        ((h_channel >= 5) & (h_channel <= 25) & (s_channel >= 30) & (v_channel >= 30)) |
        # Yellow
        ((h_channel >= 20) & (h_channel <= 40) & (s_channel >= 25) & (v_channel >= 30)) |
        # Green
        ((h_channel >= 35) & (h_channel <= 90) & (s_channel >= 25) & (v_channel >= 30)) |
        # Brown/dark (rotten)
        ((h_channel >= 5) & (h_channel <= 30) & (s_channel >= 20) & (v_channel >= 15) & (v_channel <= 150))
    )
    
    fruit_color_ratio = np.sum(fruit_pixels) / total_pixels
    
    # ===== LAYER 3: TEXTURE & NATURALNESS =====
    
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    has_texture = 80 < laplacian_var < 3000
    
    brightness_std = np.std(v_channel)
    has_shading = brightness_std > 20
    
    if brightness_std < 10:
        return False, 0, "Uniform fill"
    
    # ===== SCORING =====
    
    score = 0
    
    if fruit_color_ratio >= 0.30:
        score += 40
    elif fruit_color_ratio >= 0.15:
        score += 25
    elif fruit_color_ratio >= 0.08:
        score += 10
    
    if has_texture:
        score += 25
    if has_shading:
        score += 20
    if unique_colors > 500:
        score += 15
    elif unique_colors > 150:
        score += 10
    if num_circles <= 1:
        score += 10
    if edge_ratio < 0.08:
        score += 10
    
    # ===== DECISION =====
    is_fruit = (
        score >= 40 and  # Lowered from 45 for better fruit acceptance
        fruit_color_ratio >= 0.06 and  # Lowered from 0.08 for dark rotten fruits
        num_circles < 3 and  # Allow 0-2 circles (fruits can have circular highlights)
        edge_ratio < 0.30 and  # Increased tolerance
        (num_lines <= 30 or edge_ratio < 0.15)  # Lines OK if edges are low
    )
    
    confidence = min(100, max(0, score))
    reason = f"Score:{score}, Colors:{fruit_color_ratio*100:.0f}%, Circles:{num_circles}"
    
    print(f"[Fruit Detection] Score: {score}/100 | Is Fruit: {is_fruit}")
    print(f"[Details] Colors:{fruit_color_ratio*100:.1f}% | Circles:{num_circles} | EdgeRatio:{edge_ratio*100:.1f}%")
    
    return is_fruit, confidence, reason

@app.route('/')
def index():
    return render_template('index.html', 
                         freshness_levels=FRESHNESS_LEVELS,
                         freshness_info=FRESHNESS_INFO)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # PRE-CHECK: Verify it's actually a fruit
            is_fruit, fruit_confidence, reason = is_fruit_like(filepath)
            
            print(f"[Upload] File: {filename} | Fruit Check: {is_fruit} (Score: {fruit_confidence}/100)")
            
            if not is_fruit:
                os.remove(filepath)
                print(f"[REJECTED] Not a fruit - {reason}")
                return jsonify({
                    'error': '⚠️ This is not a fruit image! Please upload a real fruit photo.'
                }), 400
            
            image_hash = calculate_image_hash(filepath)
            
            # CHECK FOR ROTTEN FEATURES FIRST
            is_rotten, rot_score, rot_details = detect_rotten_features(filepath)
            print(f"[Rot Detection] Score: {rot_score}/100 | Is Rotten: {is_rotten}")
            print(f"[Rot Details] {rot_details}")
            
            # Preprocess image using OpenCV
            processed_image = preprocess_image(filepath)
            
            # Make prediction
            if model is None:
                return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
            
            predictions = model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx]) * 100
            
            # OVERRIDE: If clear rot detected, force Rotten classification
            if is_rotten:
                predicted_class_idx = 4  # Rotten is index 4
                confidence = min(rot_score, 100)  # Cap at 100%
                print(f"[OVERRIDE] Rotten features detected! Overriding to Rotten ({confidence}%)")
                
                # Override predictions array to reflect rotten
                predictions = np.zeros((1, 5))
                predictions[0][4] = confidence / 100.0  # Rotten
                predictions[0][0] = (100 - confidence) / 100.0  # Fresh gets remainder
            
            # CONFIDENCE THRESHOLD CHECK
            CONFIDENCE_THRESHOLD = 45.0  # Reject if confidence < 45%
            
            if confidence < CONFIDENCE_THRESHOLD:
                os.remove(filepath)
                return jsonify({
                    'error': '⚠️ Image quality too poor. Please upload a clearer fruit photo.'
                }), 400
            
            # Ensure confidence is capped at 100%
            confidence = min(confidence, 100.0)
            
            predicted_freshness = FRESHNESS_LEVELS[predicted_class_idx]
            freshness_details = FRESHNESS_INFO[predicted_freshness]
            
            # Get top 3 predictions
            top_3_idx = np.argsort(predictions[0])[-3:][::-1]
            top_3_predictions = [
                {
                    'level': FRESHNESS_LEVELS[idx],
                    'confidence': min(float(predictions[0][idx]) * 100, 100.0),  # Cap at 100%
                    'color': FRESHNESS_INFO[FRESHNESS_LEVELS[idx]]['color']
                }
                for idx in top_3_idx
            ]
            
            block_data = {
                'type': 'freshness_check',
                'image_hash': image_hash,
                'filename': filename,
                'freshness_level': predicted_freshness,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            new_block = blockchain.add_block(block_data)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'freshness_level': predicted_freshness,
                'confidence': confidence,
                'emoji': freshness_details['emoji'],
                'color': freshness_details['color'],
                'description': freshness_details['description'],
                'recommendation': freshness_details['recommendation'],
                'top_predictions': top_3_predictions,
                'blockchain_record': {  # Include blockchain info in response
                    'block_index': new_block.index,
                    'block_hash': new_block.hash,
                    'image_hash': image_hash
                }
            })
        
        except Exception as e:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """Get recent blockchain records"""
    recent_records = blockchain.get_recent_records(limit=20)
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        'records': recent_records,
        'total_blocks': len(blockchain.chain),
        'is_valid': is_valid
    })

@app.route('/blockchain/verify', methods=['GET'])
def verify_blockchain():
    """Verify blockchain integrity"""
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        'is_valid': is_valid,
        'total_blocks': len(blockchain.chain),
        'message': 'Blockchain is valid and secure' if is_valid else 'Blockchain integrity compromised!'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
