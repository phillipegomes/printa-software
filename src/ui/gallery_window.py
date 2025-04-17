# src/ui/gallery_window.py

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.ui.main_actions import carregar_imagens

class GalleryWindow(QWidget):
    def __init__(self, evento_path, main_window=None):
        super().__init__()
        self.setWindowTitle("Galeria de Fotos")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        layout = QVBoxLayout()
        self.fotos_path = os.path.join(evento_path, "Fotos")

        imagens = carregar_imagens(self.fotos_path)
        for path in imagens:
            label = QLabel()
            label.setPixmap(QPixmap(path).scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))
            layout.addWidget(label)

        self.setLayout(layout)
