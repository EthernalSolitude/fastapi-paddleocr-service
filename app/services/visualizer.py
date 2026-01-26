import io
import numpy as np
import fitz
from PIL import Image, ImageDraw, ImageFont
from app.core.config import settings

def create_side_by_side_image(img_np: np.ndarray, boxes, texts, scores) -> Image.Image:
    """Рисует картинку: Слева оригинал, Справа текст"""
    
    left_image = Image.fromarray(img_np)
    left_draw = ImageDraw.Draw(left_image)
    
    right_image = Image.new("RGB", left_image.size, (255, 255, 255))
    right_draw = ImageDraw.Draw(right_image)

    try:
        base_font_size = 20
        font = ImageFont.truetype(settings.FONT_PATH, base_font_size)
        font_path = settings.FONT_PATH
    except IOError:
        font = ImageFont.load_default()
        font_path = None

    for box, text, score in zip(boxes, texts, scores):
        if score < settings.MIN_SCORE: continue

        if isinstance(box, list) or isinstance(box, np.ndarray):
             points = [tuple(point) for point in box]
             
             left_draw.polygon(points, outline="red", width=2)
             
             box_height = abs(box[3][1] - box[0][1])
             current_font = font
             if font_path and box_height > 8:
                 try:
                     current_font = ImageFont.truetype(font_path, int(box_height * 0.8))
                 except: pass

             txt_x, txt_y = points[0]
             right_draw.text((txt_x, txt_y), text, fill="black", font=current_font)
             right_draw.polygon(points, outline="#E0E0E0", width=1)

    # Склейка
    total_width = left_image.width + right_image.width
    combined_image = Image.new("RGB", (total_width, left_image.height))
    combined_image.paste(left_image, (0, 0))
    combined_image.paste(right_image, (left_image.width, 0))
    
    return combined_image

def append_image_to_pdf(pdf_doc: fitz.Document, pil_image: Image.Image):

    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format="PNG")
    img_data = img_bytes.getvalue()
    
    width, height = pil_image.width, pil_image.height
    new_page = pdf_doc.new_page(width=width, height=height)
    
    new_page.insert_image(new_page.rect, stream=img_data)
    
    img_bytes.close()
