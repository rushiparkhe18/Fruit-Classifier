import cv2
import numpy as np

def is_fruit_like_optimized(image_path):
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
    
    # Detect rectangles and squares (boxes, packages, screens, books)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rectangular_objects = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500:  # Ignore tiny contours
            continue
        
        # Approximate contour to polygon
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Check if it's a rectangle/square (4 corners)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Rectangle or square (aspect ratio between 0.5 and 2.0)
            if 0.5 <= aspect_ratio <= 2.0 and area > (total_pixels * 0.05):
                rectangular_objects += 1
    
    # Reject if multiple large rectangles/squares detected
    if rectangular_objects >= 2:
        return False, 0, "Rectangular objects detected"
    
    edge_ratio = np.sum(edges > 0) / total_pixels
    
    # Check for sharp edges
    if edge_ratio > 0.25:
        return False, 0, "Mechanical object"
    
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
    if rectangular_objects == 0:
        score += 10
    if edge_ratio < 0.08:
        score += 10
    
    # ===== DECISION =====
    is_fruit = (
        score >= 45 and
        fruit_color_ratio >= 0.08 and
        rectangular_objects < 2 and
        edge_ratio < 0.25
    )
    
    confidence = min(100, max(0, score))
    reason = f"Score:{score}, Colors:{fruit_color_ratio*100:.0f}%, Rectangles:{rectangular_objects}"
    
    return is_fruit, confidence, reason
