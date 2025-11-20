"""
Standalone Fruit Freshness Classifier - Native Android App
100% Offline - No server dependency
Uses TensorFlow Lite for fast mobile inference
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock
import numpy as np
import cv2
import os
import hashlib
from datetime import datetime
import json

# TensorFlow Lite import
try:
    import tensorflow as tf
    TFLITE_AVAILABLE = True
except ImportError:
    TFLITE_AVAILABLE = False

# Blockchain implementation (lightweight for mobile)
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0, datetime.now().isoformat(), {"type": "genesis"}, "0")
    
    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), datetime.now().isoformat(), data, previous_block.hash)
        self.chain.append(new_block)
        return new_block

# Main App
class FruitClassifierApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blockchain = Blockchain()
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.current_image_path = None
        
        self.FRESHNESS_LEVELS = [
            'Fresh',
            'Slightly Ripe',
            'Ripe',
            'Overripe',
            'Rotten'
        ]
        
        self.FRESHNESS_INFO = {
            'Fresh': {'emoji': '✨', 'color': (0.06, 0.73, 0.51, 1), 'desc': 'Perfect condition!'},
            'Slightly Ripe': {'emoji': '🌟', 'color': (0.52, 0.80, 0.09, 1), 'desc': 'Good condition'},
            'Ripe': {'emoji': '⚠️', 'color': (0.96, 0.62, 0.04, 1), 'desc': 'Consume soon'},
            'Overripe': {'emoji': '⏰', 'color': (0.98, 0.45, 0.09, 1), 'desc': 'Use immediately'},
            'Rotten': {'emoji': '❌', 'color': (0.94, 0.27, 0.27, 1), 'desc': 'Discard'}
        }
    
    def build(self):
        Window.clearcolor = (0.06, 0.73, 0.51, 1)  # Green background
        
        # Load TFLite model
        self.load_model()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(
            text='🍎 Fruit Freshness Classifier\n100% Offline AI',
            font_size='24sp',
            size_hint_y=0.15,
            bold=True,
            color=(1, 1, 1, 1)
        )
        layout.add_widget(header)
        
        # Image preview
        self.image_preview = KivyImage(
            size_hint_y=0.4,
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.image_preview)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        select_btn = Button(
            text='📁 Select Image',
            background_color=(0.06, 0.73, 0.51, 1),
            font_size='18sp',
            bold=True
        )
        select_btn.bind(on_press=self.select_image)
        btn_layout.add_widget(select_btn)
        
        self.predict_btn = Button(
            text='🔍 Analyze',
            background_color=(0.04, 0.59, 0.41, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.predict_btn.bind(on_press=self.predict_freshness)
        btn_layout.add_widget(self.predict_btn)
        
        layout.add_widget(btn_layout)
        
        # Results
        self.result_label = Label(
            text='Select a fruit image to analyze',
            font_size='20sp',
            size_hint_y=0.3,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        layout.add_widget(self.result_label)
        
        return layout
    
    def load_model(self):
        """Load TensorFlow Lite model"""
        try:
            model_path = 'fruit_freshness_model.tflite'
            if not os.path.exists(model_path):
                self.result_label.text = '❌ Model file not found!'
                return
            
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print("✅ TFLite model loaded successfully!")
        except Exception as e:
            self.result_label.text = f'❌ Error loading model: {str(e)}'
    
    def select_image(self, instance):
        """Open file chooser to select image"""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path=os.path.expanduser('~')
        )
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(filechooser)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select Fruit Image',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(btn):
            if filechooser.selection:
                self.current_image_path = filechooser.selection[0]
                self.image_preview.source = self.current_image_path
                self.predict_btn.disabled = False
                self.result_label.text = 'Image loaded! Tap Analyze.'
            popup.dismiss()
        
        def on_cancel(btn):
            popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=on_cancel)
        
        popup.open()
    
    def preprocess_image(self, image_path):
        """Preprocess image for TFLite model"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict_freshness(self, instance):
        """Run inference on selected image"""
        if not self.current_image_path or not self.interpreter:
            self.result_label.text = '❌ No image selected or model not loaded'
            return
        
        try:
            self.result_label.text = '⏳ Analyzing...'
            
            # Preprocess image
            input_data = self.preprocess_image(self.current_image_path)
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            
            # Get result
            predicted_idx = np.argmax(predictions)
            confidence = float(predictions[predicted_idx]) * 100
            freshness_level = self.FRESHNESS_LEVELS[predicted_idx]
            info = self.FRESHNESS_INFO[freshness_level]
            
            # Add to blockchain
            image_hash = hashlib.sha256(open(self.current_image_path, 'rb').read()).hexdigest()[:16]
            block_data = {
                'type': 'freshness_check',
                'image_hash': image_hash,
                'freshness_level': freshness_level,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            new_block = self.blockchain.add_block(block_data)
            
            # Display result
            result_text = f"{info['emoji']} {freshness_level}\n\n"
            result_text += f"Confidence: {confidence:.1f}%\n\n"
            result_text += f"{info['desc']}\n\n"
            result_text += f"🔗 Blockchain: Block #{new_block.index}\n"
            result_text += f"Hash: {new_block.hash[:16]}..."
            
            self.result_label.text = result_text
            
            # Change background color based on result
            Window.clearcolor = info['color']
            
        except Exception as e:
            self.result_label.text = f'❌ Error: {str(e)}'

if __name__ == '__main__':
    FruitClassifierApp().run()
