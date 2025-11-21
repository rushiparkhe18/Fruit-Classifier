"""
SIMPLE & ROBUST: Fruit Freshness Classifier
Works with minimal data using data augmentation
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
import os

print("=" * 80)
print("🍎 SIMPLE FRUIT FRESHNESS MODEL")
print("=" * 80)

CATEGORIES = ['Fresh', 'Slightly Ripe', 'Ripe', 'Overripe', 'Rotten']
IMG_SIZE = 128

def load_images_from_folder(folder='training_data'):
    """Load all images from organized folders"""
    images, labels = [], []
    category_mapping = {
        'fresh': 0,
        'slightly_ripe': 1,
        'ripe': 2,
        'overripe': 3,
        'rotten': 4
    }
    
    print("\n📂 Loading images...")
    for category_name, label_idx in category_mapping.items():
        category_path = os.path.join(folder, category_name)
        
        if not os.path.exists(category_path):
            print(f"  ⚠️  {category_name}/ not found")
            continue
        
        files = [f for f in os.listdir(category_path) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        print(f"  {CATEGORIES[label_idx]}: {len(files)} images")
        
        for filename in files:
            filepath = os.path.join(category_path, filename)
            try:
                img = cv2.imread(filepath)
                if img is None:
                    continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = img.astype('float32') / 255.0
                
                images.append(img)
                labels.append(label_idx)
            except:
                pass
    
    return np.array(images), np.array(labels)

def augment_data(images, labels, factor=15):  # Reduced from 20 to 15
    """Generate more training data through augmentation"""
    print(f"\n🔄 Augmenting data (x{factor})...")
    
    augmented_images, augmented_labels = [], []
    
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.3,
        height_shift_range=0.3,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.6, 1.4],
        fill_mode='nearest'
    )
    
    for img, label in zip(images, labels):
        augmented_images.append(img)
        augmented_labels.append(label)
        
        img_expanded = np.expand_dims(img, 0)
        count = 0
        for batch in datagen.flow(img_expanded, batch_size=1):
            augmented_images.append(batch[0])
            augmented_labels.append(label)
            count += 1
            if count >= factor:
                break
    
    print(f"  Generated {len(augmented_images)} total images")
    return np.array(augmented_images), np.array(augmented_labels)

def create_model():
    """Simple but effective CNN"""
    model = keras.Sequential([
        # Input
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        
        # Conv Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Conv Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Conv Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Conv Block 4
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),
        
        # Classification
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(5, activation='softmax')
    ])
    
    return model

def main():
    # Load data
    X, y = load_images_from_folder()
    
    if len(X) == 0:
        print("\n❌ No training data found!")
        print("\n👉 Run: python setup_training_data.py")
        return
    
    print(f"\n📊 Loaded {len(X)} images")
    
    # Show distribution
    unique, counts = np.unique(y, return_counts=True)
    for idx, count in zip(unique, counts):
        print(f"  {CATEGORIES[idx]}: {count}")
    
    # Augment if too few images
    if len(X) < 100:
        X, y = augment_data(X, y, factor=15)  # Reduced augmentation for speed
    
    # Shuffle
    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]
    
    # Split
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]
    
    print(f"\n📊 Train: {len(X_train)} | Val: {len(X_val)}")
    
    # Build model
    print("\n🔨 Building model...")
    model = create_model()
    
    model.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    print("\n🚀 Training...")
    print("-" * 80)
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=15,  # Fast training - only 15 epochs
        batch_size=32,
        callbacks=[
            keras.callbacks.EarlyStopping(
                patience=5,  # Stop if no improvement after 5 epochs
                restore_best_weights=True,
                monitor='val_accuracy',
                mode='max'
            ),
            keras.callbacks.ReduceLROnPlateau(
                patience=3,  # Reduce LR faster
                factor=0.5,
                min_lr=1e-7,
                monitor='val_loss'
            )
        ],
        verbose=1
    )
    
    # Evaluate
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\n📈 Validation Accuracy: {val_acc*100:.2f}%")
    
    # Save
    model.save('fruit_freshness_model.h5')
    print("✅ Model saved: fruit_freshness_model.h5")
    
    # Test
    print("\n🧪 Testing predictions:")
    for i in range(min(5, len(X_val))):
        pred = model.predict(np.expand_dims(X_val[i], 0), verbose=0)
        pred_class = np.argmax(pred[0])
        conf = pred[0][pred_class] * 100
        true_class = y_val[i]
        
        status = "✅" if pred_class == true_class else "❌"
        print(f"  {status} True: {CATEGORIES[true_class]:15s} | Pred: {CATEGORIES[pred_class]:15s} ({conf:.0f}%)")
    
    print("\n" + "=" * 80)
    print("🎉 Done! Your model is ready to use.")
    print("=" * 80)

if __name__ == "__main__":
    main()
