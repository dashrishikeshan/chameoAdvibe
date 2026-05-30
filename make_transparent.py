import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import urllib.request

def load_clean_icon(path, size):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    b, g, r, a = cv2.split(img)
    rgb = cv2.merge((b,g,r))
    
    mask = (a == 0).astype(np.uint8) * 255
    band = cv2.dilate((a > 0).astype(np.uint8)*255, np.ones((11,11), np.uint8))
    inpaint_mask = cv2.bitwise_and(mask, band)
    
    rgb_inpainted = cv2.inpaint(rgb, inpaint_mask, 5, cv2.INPAINT_TELEA)
    clean_img = cv2.merge((rgb_inpainted[:,:,0], rgb_inpainted[:,:,1], rgb_inpainted[:,:,2], a))
    
    pil_img = Image.fromarray(cv2.cvtColor(clean_img, cv2.COLOR_BGRA2RGBA))
    return pil_img.resize((size, size), Image.Resampling.LANCZOS)

def build_logo():
    font_path = "Montserrat-ExtraBoldItalic.ttf"
    if not os.path.exists(font_path):
        urllib.request.urlretrieve("https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBoldItalic.ttf", font_path)
        
    width, height = 4800, 3200
    # Fully transparent background
    bg = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    
    icon_size = 2200
    icon = load_clean_icon('assets/chameo-icon-transparent.png', icon_size)
    
    icon_x = (width - icon_size) // 2
    icon_y = 300
    bg.paste(icon, (icon_x, icon_y), icon)
    
    draw = ImageDraw.Draw(bg)
    font_size = 400
    font = ImageFont.truetype(font_path, font_size)
    
    text1 = "CHAMEO "
    text2 = "MEDIA"
    
    bbox1 = draw.textbbox((0, 0), text1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    
    total_w = w1 + w2
    start_x = (width - total_w) // 2
    text_y = icon_y + icon_size + 40
    
    # Theme text colors: --blue-deep (#083c72) and --green (#18bd32)
    color1 = (8, 60, 114, 255)
    color2 = (24, 189, 50, 255)
    
    draw.text((start_x, text_y), text1, font=font, fill=color1)
    draw.text((start_x + w1, text_y), text2, font=font, fill=color2)
    
    bbox = bg.getbbox()
    if bbox:
        pad = 50
        bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(width, bbox[2] + pad),
            min(height, bbox[3] + pad)
        )
        bg = bg.crop(bbox)

    bg.save('assets/chameo-logo.png')
    
    jpeg_bg = Image.new('RGB', bg.size, (255, 255, 255))
    jpeg_bg.paste(bg, (0, 0), bg)
    jpeg_bg.save('assets/chameo-logo.jpeg', quality=100)
    print("Transparent logo updated.")

if __name__ == "__main__":
    build_logo()
