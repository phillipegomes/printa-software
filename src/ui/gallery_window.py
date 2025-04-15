from PyQt6.QtWidgets import QMainWindow, QLabel, QScrollArea, QWidget, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class GalleryWindow(QMainWindow):
    def __init__(self, fotos_path):
        super().__init__()
        self.setWindowTitle("Galeria de Fotos")
        self.setGeometry(200, 100, 1000, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.fotos_path = fotos_path

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        self.grid_layout = QGridLayout(container)

        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

        self.load_gallery_images()

    def load_gallery_images(self):
        if not os.path.exists(self.fotos_path):
            return

        images = [
            f for f in sorted(os.listdir(self.fotos_path), reverse=True)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        row, col = 0, 0
        for img in images:
            full_path = os.path.join(self.fotos_path, img)
            label = QLabel()
            label.setPixmap(QPixmap(full_path).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            label.setStyleSheet("border: 1px solid #333; margin: 8px;")
            self.grid_layout.addWidget(label, row, col)

            col += 1
            if col >= 4:
                col = 0
                row += 1
