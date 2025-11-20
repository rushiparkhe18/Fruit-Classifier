from PIL import Image, ImageDraw, ImageFont
import os

# Create img directory if it doesn't exist
os.makedirs('static/img', exist_ok=True)

def create_icon(size):
    """Create a simple fruit classifier icon"""
    # Create image with green background
    img = Image.new('RGBA', (size, size), color=(16, 185, 129, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle background
    padding = size // 10
    draw.ellipse([padding, padding, size-padding, size-padding], fill='white')
    
    # Draw text/emoji in center
    try:
        # Try to use a large font
        font_size = size // 2
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw fruit emoji or text
    text = "🍎"
    
    # Get text bbox to center it
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2)
        draw.text(position, text, fill=(16, 185, 129, 255), font=font)
    except:
        # Fallback for older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)
        position = ((size - text_width) // 2, (size - text_height) // 2)
        draw.text(position, text, fill=(16, 185, 129, 255), font=font)
    
    # Save icon
    filename = f'static/img/icon-{size}.png'
    img.save(filename)
    print(f"✅ Created {filename}")

# Create icons
print("Creating app icons...")
create_icon(192)
create_icon(512)

# Create favicon
icon_16 = Image.new('RGBA', (16, 16), color=(16, 185, 129, 255))
icon_16.save('static/img/favicon.ico')
print("✅ Created static/img/favicon.ico")

# Create a simple screenshot placeholder
screenshot = Image.new('RGB', (540, 720), color=(16, 185, 129, 255))
draw = ImageDraw.Draw(screenshot)
try:
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()

text = "Fruit Freshness\nClassifier"
draw.text((50, 300), text, fill='white', font=font, align='center')
screenshot.save('static/img/screenshot1.png')
print("✅ Created static/img/screenshot1.png")

print("\n✅ All icons created successfully!")
print("Icons are located in: static/img/")
