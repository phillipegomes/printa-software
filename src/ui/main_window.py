
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QListWidget,
    QListWidgetItem
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.modules.file_watcher import FileWatcher
from src.modules.image_loader import load_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print A - Bloco 1")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.image_label = QLabel("Aguardando imagem...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setFixedHeight(140)
        self.thumbnail_list.setStyleSheet("background-color: #2e2e2e;")
        self.thumbnail_list.itemClicked.connect(self.display_selected_image)
        self.main_layout.addWidget(self.thumbnail_list)

        self.image_paths = []
        self.event_folder = "eventos/Evento_Teste/Fotos"
        os.makedirs(self.event_folder, exist_ok=True)

        self.watcher = FileWatcher(self.event_folder, self.add_new_image)
        self.watcher.start()

    def add_new_image(self, image_path):
        self.image_paths.append(image_path)
        self.display_image(image_path)

        item = QListWidgetItem()
        thumb = QPixmap(image_path).scaledToHeight(100)
        item.setIcon(thumb)
        self.thumbnail_list.addItem(item)

    def display_image(self, image_path):
        pixmap = load_image(image_path).scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def display_selected_image(self, item):
        index = self.thumbnail_list.row(item)
        image_path = self.image_paths[index]
        self.display_image(image_path)
