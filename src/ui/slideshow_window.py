
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

class SlideshowWindow(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle("Galeria")
        self.setStyleSheet("background-color: black;")
        self.setGeometry(100, 100, 1000, 700)

        self.image_paths = image_paths
        self.current_index = 0

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        self.update_image()

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)  # muda a imagem a cada 3 segundos

    def update_image(self):
        if self.image_paths:
            pixmap = QPixmap(self.image_paths[self.current_index]).scaled(
                self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.update_image()
