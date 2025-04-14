
from PIL import Image
from PyQt6.QtGui import QPixmap
import pillow_heif

def load_image(path):
    if path.lower().endswith(".heic"):
        heif_file = pillow_heif.read_heif(path)
        img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
    else:
        img = Image.open(path)
    img = img.convert("RGB")
    return QPixmap(path)
