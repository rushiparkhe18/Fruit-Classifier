"""
FIXED: Balanced Fruit Freshness Classifier
- Handles class imbalance with weights
- Better augmentation
- More robust training
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
import os
from sklearn.utils.class_weight import compute_class_weight

print("=" * 80)
print("🍎 BALANCED FRUIT FRESHNESS MODEL")
print("=" * 80)

CATEGORIES = ['Fresh', 'Slightly Ripe', 'Ripe', 'Overripe', 'Rotten']
IMG_SIZE = 128

def load_images_from_folder(folder='training_data'):
    """Load all images"""
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

def create_balanced_dataset(images, labels):
    """Balance dataset by oversampling minority classes"""
    print("\n⚖️  Balancing dataset...")
    
    unique_labels, counts = np.unique(labels, return_counts=True)
    max_count = max(counts)
    
    balanced_images = []
    balanced_labels = []
    
    for label_idx in unique_labels:
        # Get all images for this class
        class_mask = labels == label_idx
        class_images = images[class_mask]
        
        # Current count vs target
        current = len(class_images)
        target = max_count * 3  # Triple the max for good augmentation
        
        # Add original images
        balanced_images.extend(class_images)
        balanced_labels.extend([label_idx] * current)
        
        # Augment to reach target
        if current < target:
            needed = target - current
            
            from tensorflow.keras.preprocessing.image import ImageDataGenerator
            datagen = ImageDataGenerator(
                rotation_range=45,
                width_shift_range=0.3,
                height_shift_range=0.3,
                shear_range=0.3,
                zoom_range=0.4,
                horizontal_flip=True,
                vertical_flip=True,
                brightness_range=[0.5, 1.5],
                fill_mode='nearest'
            )
            
            aug_count = 0
            for img in class_images:
                if aug_count >= needed:
                    break
                    
                img_expanded = np.expand_dims(img, 0)
                per_image = (needed // current) + 1
                
                for batch in datagen.flow(img_expanded, batch_size=1):
                    balanced_images.append(batch[0])
                    balanced_labels.append(label_idx)
                    aug_count += 1
                    if aug_count >= needed:
                        break
        
        print(f"  {CATEGORIES[label_idx]}: {current} → {current + (target - current)}")
    
    indices = np.random.permutation(len(balanced_images))
    return np.array(balanced_images)[indices], np.array(balanced_labels)[indices]

def create_improved_model():
    """Improved CNN with better regularization"""
    model = keras.Sequential([
        # Input
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.4),
        
        # Global pooling
        layers.GlobalAveragePooling2D(),
        
        # Classification
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(5, activation='softmax')
    ])
    
    return model

def main():
    # Load data
    X, y = load_images_from_folder()
    
    if len(X) == 0:
        print("\n❌ No training data!")
        print("👉 Run: python setup_training_data.py")
        return
    
    print(f"\n📊 Original: {len(X)} images")
    
    # Balance dataset
    X, y = create_balanced_dataset(X, y)
    
    print(f"\n📊 Balanced: {len(X)} images")
    
    # Split
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]
    
    print(f"📊 Train: {len(X_train)} | Val: {len(X_val)}")
    
    # Compute class weights
    class_weights = compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = dict(enumerate(class_weights))
    print(f"\n⚖️  Class weights: {class_weight_dict}")
    
    # Build model
    print("\n🔨 Building improved model...")
    model = create_improved_model()
    
    model.compile(
        optimizer=keras.optimizers.Adam(0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    print("\n🚀 Training with class weights...")
    print("-" * 80)
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=25,
        batch_size=32,
        class_weight=class_weight_dict,
        callbacks=[
            keras.callbacks.EarlyStopping(
                patience=8,
                restore_best_weights=True,
                monitor='val_accuracy',
                mode='max',
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                patience=4,
                factor=0.5,
                min_lr=1e-7,
                verbose=1
            )
        ],
        verbose=1
    )
    
    # Evaluate
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\n📈 Validation Accuracy: {val_acc*100:.2f}%")
    
    # Test predictions
    print("\n🧪 Testing on validation set:")
    predictions = model.predict(X_val, verbose=0)
    
    correct = 0
    for i in range(len(X_val)):
        pred_class = np.argmax(predictions[i])
        true_class = y_val[i]
        conf = predictions[i][pred_class] * 100
        
        if pred_class == true_class:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        if i < 10:  # Show first 10
            print(f"  {status} True: {CATEGORIES[true_class]:15s} | Pred: {CATEGORIES[pred_class]:15s} ({conf:.0f}%)")
    
    print(f"\n✅ Accuracy: {correct}/{len(X_val)} = {correct/len(X_val)*100:.1f}%")
    
    # Save
    model.save('fruit_freshness_model.h5')
    print("\n💾 Model saved: fruit_freshness_model.h5")
    
    print("\n" + "=" * 80)
    print("🎉 Training complete! Model ready to use.")
    print("=" * 80)

if __name__ == "__main__":
    main()
