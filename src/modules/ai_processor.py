from PIL import Image, ImageFilter
import os

def apply_ai_filter(image_path):
    try:
        img = Image.open(image_path)
        img = img.filter(ImageFilter.CONTOUR)
        new_path = image_path.replace(".", "_IA.")
        img.save(new_path)
        return new_path
    except Exception as e:
        print(f"Erro ao aplicar IA: {e}")
        return image_path
