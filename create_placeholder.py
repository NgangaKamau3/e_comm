from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image():
    # Create a 300x300 image with a light gray background
    img = Image.new('RGB', (300, 300), color='#f0f0f0')
    
    # Get drawing context
    d = ImageDraw.Draw(img)
    
    # Draw text
    text = "No Image"
    # Use default font
    font_size = 40
    
    # Calculate text position to center it
    text_bbox = d.textbbox((0, 0), text, font_size=font_size)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (300 - text_width) / 2
    y = (300 - text_height) / 2
    
    # Draw the text
    d.text((x, y), text, fill='#666666', font_size=font_size)
    
    # Save the image
    img.save('static/images/placeholder.png')

if __name__ == '__main__':
    create_placeholder_image()