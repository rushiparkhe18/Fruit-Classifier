"""
Fruit Freshness Classifier - Mobile App (Kivy)
Optimized for Android APK
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
import cv2
import numpy as np
import tensorflow as tf
from datetime import datetime
import os
import hashlib
import json

# Set window size for testing (remove for mobile)
# Window.size = (400, 700)

# Import blockchain
from blockchain import Blockchain

# Freshness levels
FRESHNESS_LEVELS = ['Fresh', 'Slightly Ripe', 'Ripe', 'Overripe', 'Rotten']

FRESHNESS_INFO = {
    'Fresh': {
        'emoji': '✨',
        'color': [0.06, 0.73, 0.51, 1],  # #10b981
        'description': 'Perfect condition! Best time to consume.',
        'recommendation': 'Enjoy now or store properly for later use.'
    },
    'Slightly Ripe': {
        'emoji': '🌟',
        'color': [0.52, 0.80, 0.09, 1],  # #84cc16
        'description': 'Good condition with optimal ripeness.',
        'recommendation': 'Great for eating! Consume within 2-3 days.'
    },
    'Ripe': {
        'emoji': '⚠️',
        'color': [0.96, 0.62, 0.04, 1],  # #f59e0b
        'description': 'Fully ripe. Should be consumed soon.',
        'recommendation': 'Eat within 1-2 days or use in cooking.'
    },
    'Overripe': {
        'emoji': '⏰',
        'color': [0.98, 0.45, 0.09, 1],  # #f97316
        'description': 'Past peak freshness. Quality declining.',
        'recommendation': 'Use immediately in smoothies or baking.'
    },
    'Rotten': {
        'emoji': '❌',
        'color': [0.94, 0.27, 0.27, 1],  # #ef4444
        'description': 'Spoiled. Not safe for consumption.',
        'recommendation': 'Discard immediately. Do not consume.'
    }
}


class FruitClassifierApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None
        self.blockchain = Blockchain()
        self.current_image_path = None
        
    def build(self):
        self.title = 'Fruit Freshness Classifier'
        
        # Load model
        try:
            self.model = tf.keras.models.load_model('fruit_freshness_model.h5')
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Set background color
        with layout.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Header
        header = Label(
            text='[b]🍎 Fruit Freshness Classifier[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size=dp(24),
            color=[0.2, 0.2, 0.3, 1]
        )
        layout.add_widget(header)
        
        # Image preview area
        self.image_preview = KivyImage(
            source='',
            size_hint_y=0.35,
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.image_preview)
        
        # Select Image Button
        self.select_btn = Button(
            text='📷 Select Fruit Image',
            size_hint_y=0.08,
            background_color=[0.2, 0.5, 0.9, 1],
            font_size=dp(18),
            bold=True
        )
        self.select_btn.bind(on_press=self.select_image)
        layout.add_widget(self.select_btn)
        
        # Analyze Button
        self.analyze_btn = Button(
            text='🔍 Analyze Freshness',
            size_hint_y=0.08,
            background_color=[0.1, 0.7, 0.5, 1],
            font_size=dp(18),
            bold=True,
            disabled=True
        )
        self.analyze_btn.bind(on_press=self.analyze_fruit)
        layout.add_widget(self.analyze_btn)
        
        # Results area (scrollable)
        scroll = ScrollView(size_hint_y=0.35)
        self.result_label = Label(
            text='Select an image to begin analysis...',
            markup=True,
            size_hint_y=None,
            font_size=dp(16),
            color=[0.3, 0.3, 0.4, 1],
            padding=[dp(15), dp(15)]
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        # Blockchain button
        blockchain_btn = Button(
            text='🔗 View Blockchain Records',
            size_hint_y=0.06,
            background_color=[0.3, 0.3, 0.4, 1],
            font_size=dp(14)
        )
        blockchain_btn.bind(on_press=self.show_blockchain)
        layout.add_widget(blockchain_btn)
        
        return layout
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def select_image(self, instance):
        """Open file chooser to select image"""
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        filechooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path=os.path.expanduser('~')
        )
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        
        select_btn = Button(text='Select', background_color=[0.1, 0.7, 0.5, 1])
        cancel_btn = Button(text='Cancel', background_color=[0.7, 0.3, 0.3, 1])
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(filechooser)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select Fruit Image',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(instance):
            if filechooser.selection:
                self.current_image_path = filechooser.selection[0]
                self.image_preview.source = self.current_image_path
                self.analyze_btn.disabled = False
                self.result_label.text = '[b]Image loaded! Tap "Analyze Freshness"[/b]'
                popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def preprocess_image(self, image_path):
        """Preprocess image for model"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, (128, 128))
        img_normalized = img_resized.astype('float32') / 255.0
        img_batch = np.expand_dims(img_normalized, axis=0)
        return img_batch
    
    def detect_rotten_features(self, image_path):
        """Enhanced rotten detection"""
        from app import detect_rotten_features
        return detect_rotten_features(image_path)
    
    def is_fruit_like(self, image_path):
        """Validate if image is a fruit"""
        from app import is_fruit_like
        return is_fruit_like(image_path)
    
    def analyze_fruit(self, instance):
        """Analyze the selected fruit image"""
        if not self.current_image_path:
            self.show_error("No image selected!")
            return
        
        if self.model is None:
            self.show_error("Model not loaded!")
            return
        
        self.result_label.text = '[b]Analyzing...[/b]'
        
        # Schedule analysis to not block UI
        Clock.schedule_once(lambda dt: self._perform_analysis(), 0.1)
    
    def _perform_analysis(self):
        """Perform the actual analysis"""
        try:
            # Validate it's a fruit
            is_fruit, confidence, reason = self.is_fruit_like(self.current_image_path)
            
            if not is_fruit:
                self.show_error("⚠️ This is not a fruit image!\nPlease select a real fruit photo.")
                return
            
            # Check for rotten features
            is_rotten, rot_score, rot_details = self.detect_rotten_features(self.current_image_path)
            
            # Preprocess and predict
            processed_image = self.preprocess_image(self.current_image_path)
            predictions = self.model.predict(processed_image, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx]) * 100
            
            # Override if rotten detected
            if is_rotten:
                predicted_class_idx = 4  # Rotten
                confidence = min(rot_score, 100)
                predictions = np.zeros((1, 5))
                predictions[0][4] = confidence / 100.0
                predictions[0][0] = (100 - confidence) / 100.0
            
            confidence = min(confidence, 100.0)
            
            # Get result
            predicted_freshness = FRESHNESS_LEVELS[predicted_class_idx]
            freshness_info = FRESHNESS_INFO[predicted_freshness]
            
            # Calculate image hash
            with open(self.current_image_path, 'rb') as f:
                image_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Add to blockchain
            block_data = {
                'type': 'freshness_check',
                'image_hash': image_hash,
                'filename': os.path.basename(self.current_image_path),
                'freshness_level': predicted_freshness,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            new_block = self.blockchain.add_block(block_data)
            
            # Display results
            result_text = f"""[b][size=24]{freshness_info['emoji']} {predicted_freshness}[/size][/b]

[b]Confidence:[/b] {confidence:.1f}%

[b]Status:[/b]
{freshness_info['description']}

[b]Recommendation:[/b]
{freshness_info['recommendation']}

[b]🔗 Blockchain Record[/b]
Block #{new_block.index}
Hash: {new_block.hash[:32]}...

[b]Top Predictions:[/b]"""
            
            # Add top 3 predictions
            top_3_idx = np.argsort(predictions[0])[-3:][::-1]
            for idx in top_3_idx:
                level = FRESHNESS_LEVELS[idx]
                conf = min(float(predictions[0][idx]) * 100, 100.0)
                result_text += f"\n• {level}: {conf:.1f}%"
            
            self.result_label.text = result_text
            
        except Exception as e:
            self.show_error(f"Error during analysis:\n{str(e)}")
    
    def show_blockchain(self, instance):
        """Show blockchain records"""
        records = self.blockchain.get_recent_records(limit=10)
        
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        scroll = ScrollView()
        records_label = Label(
            text=self._format_blockchain_records(records),
            markup=True,
            size_hint_y=None,
            font_size=dp(14)
        )
        records_label.bind(texture_size=records_label.setter('size'))
        scroll.add_widget(records_label)
        
        close_btn = Button(
            text='Close',
            size_hint_y=0.1,
            background_color=[0.3, 0.3, 0.4, 1]
        )
        
        content.add_widget(scroll)
        content.add_widget(close_btn)
        
        popup = Popup(
            title=f'Blockchain Records ({len(records)} blocks)',
            content=content,
            size_hint=(0.95, 0.8)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def _format_blockchain_records(self, records):
        """Format blockchain records for display"""
        text = "[b]Recent Blockchain Records:[/b]\n\n"
        
        for record in records:
            if record['data'].get('type') == 'freshness_check':
                data = record['data']
                text += f"""[b]Block #{record['index']}[/b]
File: {data.get('filename', 'N/A')}
Result: {data.get('freshness_level', 'N/A')}
Confidence: {data.get('confidence', 0):.1f}%
Time: {data.get('timestamp', 'N/A')[:19]}
Hash: {record['hash'][:24]}...

"""
        
        return text
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title='Error',
            content=Label(text=message, markup=True),
            size_hint=(0.8, 0.3)
        )
        popup.open()


if __name__ == '__main__':
    FruitClassifierApp().run()
