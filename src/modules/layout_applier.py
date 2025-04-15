from PIL import Image
import os

def apply_layout(image_path, layout_path):
    try:
        base = Image.open(image_path).convert("RGBA")
        overlay = Image.open(layout_path).convert("RGBA")

        overlay = overlay.resize(base.size)
        combined = Image.alpha_composite(base, overlay)

        output_path = image_path.replace(".jpg", "_layout.jpg").replace(".png", "_layout.jpg")
        combined.convert("RGB").save(output_path, "JPEG", quality=95)

        return output_path
    except Exception as e:
        print(f"Erro ao aplicar layout: {e}")
        return image_path
