import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split

# Freshness levels
FRESHNESS_LEVELS = [
    'Fresh',
    'Slightly Ripe', 
    'Ripe',
    'Overripe',
    'Rotten'
]

def create_cnn_model(input_shape=(128, 128, 3), num_classes=5):
    """
    Create a CNN model for fruit freshness classification
    """
    model = keras.Sequential([
        # First Convolutional Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second Convolutional Block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third Convolutional Block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth Convolutional Block
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Flatten and Dense Layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def generate_synthetic_data(num_samples_per_class=200):
    """
    Generate synthetic fruit images with different freshness levels
    This creates images representing various stages of fruit freshness
    """
    X = []
    y = []
    
    print("Generating synthetic freshness training data...")
    
    for class_idx, freshness_level in enumerate(FRESHNESS_LEVELS):
        print(f"Generating {num_samples_per_class} samples for {freshness_level}...")
        
        for _ in range(num_samples_per_class):
            img = np.zeros((128, 128, 3), dtype=np.uint8)
            
            # Base fruit shape (generic circular fruit)
            center = (64, 64)
            radius = 40
            
            if freshness_level == 'Fresh':
                # Bright, vibrant colors - BGR FORMAT (OpenCV uses BGR!)
                colors = [
                    (60, 20, 220),    # Bright red apple (BGR: low B, low G, high R)
                    (0, 165, 255),    # Bright orange (BGR: low B, medium G, high R)
                    (0, 255, 255),    # Bright yellow banana (BGR: low B, high G, high R)
                    (0, 200, 0),      # Bright green (BGR: low B, high G, low R)
                    (20, 200, 255),   # Bright yellow-orange (mango - BGR)
                ]
                base_color = colors[np.random.randint(0, len(colors))]
                cv2.circle(img, center, radius, base_color, -1)
                # Add multiple shine/highlight spots for freshness
                cv2.circle(img, (50, 50), 15, (255, 255, 255), -1)
                cv2.circle(img, (55, 55), 8, (240, 240, 240), -1)
                # Minimal texture - very smooth and clean
                noise_level = 10
                
            elif freshness_level == 'Slightly Ripe':
                # Slightly darker, beginning to mature - still mostly bright
                colors = [
                    (40, 40, 200),    # Darker red (BGR)
                    (20, 140, 240),   # Darker orange (BGR)
                    (50, 230, 230),   # Darker yellow (BGR)
                    (0, 180, 20),     # Yellow-green (BGR)
                ]
                base_color = colors[np.random.randint(0, len(colors))]
                cv2.circle(img, center, radius, base_color, -1)
                # Few small spots
                for _ in range(4):
                    spot_x = np.random.randint(40, 88)
                    spot_y = np.random.randint(40, 88)
                    cv2.circle(img, (spot_x, spot_y), 3, (50, 100, 180), -1)  # Light brown spots
                noise_level = 18
                
            elif freshness_level == 'Ripe':
                # Deeper colors, more spots - clearly distinct from fresh
                colors = [
                    (40, 60, 180),    # Deep red (BGR)
                    (30, 120, 200),   # Deep orange (BGR)
                    (80, 200, 200),   # Deep yellow (BGR)
                    (20, 150, 120),   # Greenish-brown (BGR)
                ]
                base_color = colors[np.random.randint(0, len(colors))]
                cv2.circle(img, center, radius, base_color, -1)
                # More brown spots - clear ripening
                for _ in range(8):
                    spot_x = np.random.randint(35, 93)
                    spot_y = np.random.randint(35, 93)
                    spot_size = np.random.randint(4, 8)
                    cv2.circle(img, (spot_x, spot_y), spot_size, (43, 90, 139), -1)  # Brown spots (BGR)
                noise_level = 28
                
            elif freshness_level == 'Overripe':
                # Dull colors, many brown spots - clearly past peak
                colors = [
                    (50, 80, 150),    # Brownish red (BGR)
                    (40, 100, 160),   # Brownish orange (BGR)
                    (70, 150, 150),   # Dull brownish yellow (BGR)
                    (50, 120, 100),   # Brown-green (BGR)
                ]
                base_color = colors[np.random.randint(0, len(colors))]
                # Slightly irregular shape - starting to wrinkle
                cv2.ellipse(img, center, (radius, radius-5), 0, 0, 360, base_color, -1)
                # Many brown spots and blemishes
                for _ in range(15):
                    spot_x = np.random.randint(30, 98)
                    spot_y = np.random.randint(30, 98)
                    spot_size = np.random.randint(5, 10)
                    cv2.circle(img, (spot_x, spot_y), spot_size, (33, 67, 101), -1)  # Dark brown (BGR)
                noise_level = 38
                
            elif freshness_level == 'Rotten':
                # VERY DARK, moldy - EXTREMELY distinct from all others
                # Include both very dark AND muddy brown colors (like rotten mangoes)
                colors = [
                    (30, 40, 60),     # VERY dark brown (BGR: dark all channels)
                    (35, 45, 50),     # Dark grayish brown (BGR)
                    (25, 35, 40),     # Almost black brown (BGR)
                    (20, 30, 45),     # Very dark reddish-brown (BGR)
                    (40, 60, 80),     # Muddy brown (like rotten mango - BGR)
                    (50, 70, 90),     # Dull muddy brown (BGR)
                    (35, 55, 70),     # Dark muddy yellowish-brown (BGR)
                ]
                base_color = colors[np.random.randint(0, len(colors))]
                # Very irregular, shriveled shape - heavily deformed
                cv2.ellipse(img, center, (radius-8, radius-12), 20, 0, 360, base_color, -1)
                
                # Add some lighter muddy patches (characteristic of rotten mangoes)
                for _ in range(8):
                    patch_x = np.random.randint(30, 98)
                    patch_y = np.random.randint(30, 98)
                    patch_size = np.random.randint(8, 15)
                    muddy_colors = [
                        (45, 75, 95),    # Light muddy brown (BGR)
                        (50, 80, 100),   # Yellowish muddy (BGR)
                        (40, 70, 85),    # Grayish muddy (BGR)
                    ]
                    muddy_color = muddy_colors[np.random.randint(0, len(muddy_colors))]
                    cv2.circle(img, (patch_x, patch_y), patch_size, muddy_color, -1)
                
                # Heavy mold coverage (dark green/black spots) - LOTS of them
                for _ in range(30):
                    spot_x = np.random.randint(20, 108)
                    spot_y = np.random.randint(20, 108)
                    spot_size = np.random.randint(7, 16)
                    mold_colors = [
                        (30, 60, 40),   # Dark green mold (BGR)
                        (30, 30, 30),   # Black spots (BGR)
                        (40, 50, 60),   # Very dark brown (BGR)
                        (20, 40, 35),   # Dark greenish-black (BGR)
                        (25, 25, 25),   # Almost black (BGR)
                    ]
                    mold_color = mold_colors[np.random.randint(0, len(mold_colors))]
                    cv2.circle(img, (spot_x, spot_y), spot_size, mold_color, -1)
                
                # Deep wrinkles/texture lines - heavily textured
                for _ in range(12):
                    pt1 = (np.random.randint(30, 98), np.random.randint(30, 98))
                    pt2 = (pt1[0] + np.random.randint(-25, 25), pt1[1] + np.random.randint(-25, 25))
                    cv2.line(img, pt1, pt2, (25, 35, 45), 3)  # Very dark wrinkle lines (BGR)
                noise_level = 55  # Very high noise for decay texture
            
            # Add noise based on freshness level
            noise = np.random.randint(-noise_level, noise_level, img.shape, dtype=np.int16)
            img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            # Add random brightness variation
            brightness = np.random.uniform(0.6, 1.2)
            img = np.clip(img * brightness, 0, 255).astype(np.uint8)
            
            # Apply slight blur for older fruits
            if class_idx >= 2:  # Ripe, Overripe, Rotten
                blur_amount = class_idx - 1
                img = cv2.GaussianBlur(img, (blur_amount*2+1, blur_amount*2+1), 0)
            
            # Normalize
            img_normalized = img.astype('float32') / 255.0
            
            X.append(img_normalized)
            y.append(class_idx)
    
    return np.array(X), np.array(y)

def train_model():
    """
    Train the CNN model on synthetic freshness data
    """
    print("Creating CNN model for freshness detection...")
    model = create_cnn_model(num_classes=len(FRESHNESS_LEVELS))
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel Architecture:")
    model.summary()
    
    # Generate synthetic training data with more samples
    X, y = generate_synthetic_data(num_samples_per_class=200)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    
    # Data augmentation
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
    ])
    
    # Train model with more epochs for better learning
    print("\nTraining freshness detection model...")
    history = model.fit(
        data_augmentation(X_train),
        y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    val_loss, val_accuracy = model.evaluate(X_val, y_val)
    print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")
    
    # Save model
    model.save('fruit_freshness_model.h5')
    print("\nModel saved as 'fruit_freshness_model.h5'")
    
    return model, history

if __name__ == '__main__':
    train_model()
