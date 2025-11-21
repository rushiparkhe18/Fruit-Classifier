"""
COMPLETE REBUILD: Fruit Freshness CNN Model Training
- Proper data augmentation
- Balanced class handling
- Transfer learning with MobileNetV2
- Robust validation
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

print("=" * 80)
print("🍎 FRUIT FRESHNESS AI - Model Training")
print("=" * 80)

# Freshness categories
CATEGORIES = ['Fresh', 'Slightly Ripe', 'Ripe', 'Overripe', 'Rotten']
IMG_SIZE = 128

def create_advanced_model():
    """
    Create advanced CNN with transfer learning
    Uses MobileNetV2 as base + custom classification head
    """
    # Load pre-trained MobileNetV2 (without top layer)
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model initially
    base_model.trainable = False
    
    # Build custom classification head
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(5, activation='softmax')  # 5 freshness levels
    ])
    
    return model, base_model

def create_simple_cnn():
    """
    Fallback: Simple CNN if MobileNetV2 fails
    """
    model = keras.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Classification head
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(5, activation='softmax')
    ])
    
    return model

def load_and_preprocess_images(data_dir='images'):
    """
    Load images with robust preprocessing
    """
    print("\n📂 Loading training data...")
    
    images = []
    labels = []
    
    for class_idx, category in enumerate(CATEGORIES):
        category_path = os.path.join(data_dir, category.lower().replace(' ', '_'))
        
        if not os.path.exists(category_path):
            print(f"⚠️  Warning: {category_path} not found, skipping...")
            continue
        
        image_files = [f for f in os.listdir(category_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"  {category}: {len(image_files)} images")
        
        for img_file in image_files:
            img_path = os.path.join(category_path, img_file)
            
            try:
                # Read and preprocess
                img = cv2.imread(img_path)
                if img is None:
                    continue
                
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = img.astype('float32') / 255.0
                
                images.append(img)
                labels.append(class_idx)
                
            except Exception as e:
                print(f"  ⚠️  Error loading {img_file}: {e}")
    
    if len(images) == 0:
        raise ValueError("❌ No images loaded! Check your 'images' folder structure.")
    
    print(f"\n✅ Loaded {len(images)} total images")
    
    return np.array(images), np.array(labels)

def create_data_generators():
    """
    Create data generators with strong augmentation
    """
    train_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.7, 1.3],
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator()  # No augmentation for validation
    
    return train_datagen, val_datagen

def main():
    """
    Main training pipeline
    """
    # Load data
    try:
        X, y = load_and_preprocess_images()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📁 Expected folder structure:")
        print("   images/")
        print("     ├── fresh/")
        print("     ├── slightly_ripe/")
        print("     ├── ripe/")
        print("     ├── overripe/")
        print("     └── rotten/")
        return
    
    # Check class distribution
    print("\n📊 Class distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for idx, count in zip(unique, counts):
        print(f"  {CATEGORIES[idx]}: {count} images")
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Train: {len(X_train)} | Validation: {len(X_val)}")
    
    # Create model
    print("\n🔨 Building model...")
    try:
        model, base_model = create_advanced_model()
        use_transfer_learning = True
        print("  ✅ Using MobileNetV2 with Transfer Learning")
    except Exception as e:
        print(f"  ⚠️  MobileNetV2 failed: {e}")
        print("  ➡️  Falling back to Simple CNN")
        model = create_simple_cnn()
        use_transfer_learning = False
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n📋 Model Summary:")
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Data augmentation
    train_datagen, val_datagen = create_data_generators()
    
    # Train
    print("\n🚀 Starting training...")
    print("-" * 80)
    
    history = model.fit(
        train_datagen.flow(X_train, y_train, batch_size=32),
        validation_data=val_datagen.flow(X_val, y_val, batch_size=32),
        epochs=100,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tune if using transfer learning
    if use_transfer_learning:
        print("\n🔧 Fine-tuning with unfrozen base model...")
        base_model.trainable = True
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        history_fine = model.fit(
            train_datagen.flow(X_train, y_train, batch_size=32),
            validation_data=val_datagen.flow(X_val, y_val, batch_size=32),
            epochs=50,
            callbacks=callbacks,
            verbose=1
        )
    
    # Save final model
    model.save('fruit_freshness_model.h5')
    print("\n✅ Model saved: fruit_freshness_model.h5")
    
    # Evaluate
    print("\n📈 Final Evaluation:")
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"  Validation Accuracy: {val_acc*100:.2f}%")
    print(f"  Validation Loss: {val_loss:.4f}")
    
    # Test predictions
    print("\n🧪 Sample Predictions:")
    sample_indices = np.random.choice(len(X_val), min(5, len(X_val)), replace=False)
    for idx in sample_indices:
        pred = model.predict(np.expand_dims(X_val[idx], axis=0), verbose=0)
        pred_class = np.argmax(pred[0])
        confidence = pred[0][pred_class] * 100
        true_class = y_val[idx]
        
        status = "✅" if pred_class == true_class else "❌"
        print(f"  {status} True: {CATEGORIES[true_class]:15s} | Pred: {CATEGORIES[pred_class]:15s} ({confidence:.1f}%)")
    
    print("\n" + "=" * 80)
    print("🎉 Training Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
