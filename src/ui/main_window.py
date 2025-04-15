
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
import os

from src.modules.config_manager import ConfigManager
from src.modules.whatsapp_sender import WhatsAppSender
from src.ui.config_window import ConfigWindow
from src.ui.slideshow_window import SlideshowWindow

class MainWindow(QMainWindow):
    def __init__(self, evento_path):
        super().__init__()
        self.setWindowTitle("Print A – Evento")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        self.evento_path = evento_path
        self.fotos_path = os.path.join(self.evento_path, "Fotos")
        self.config = ConfigManager(evento_path).load_config()
        self.whatsapp = WhatsAppSender(self.config.get("whatsapp", {}))

        self.image_paths = []
        self.current_image_path = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.create_top_bar()
        self.create_image_area()
        self.create_thumbnail_area()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_new_images)
        self.timer.start(2000)

    def create_top_bar(self):
        top_bar = QHBoxLayout()

        btn_voltar = QPushButton("⬅ Voltar")
        btn_voltar.setFixedHeight(40)
        btn_voltar.clicked.connect(self.voltar_para_eventos)
        btn_voltar.setStyleSheet("padding: 8px; font-weight: bold;")

        btn_config = QPushButton("⚙ Configurações")
        btn_config.setFixedHeight(40)
        btn_config.clicked.connect(self.abrir_configuracoes)
        btn_config.setStyleSheet("padding: 8px; font-weight: bold;")

        btn_galeria = QPushButton("🖼️ Galeria")
        btn_galeria.setFixedHeight(40)
        btn_galeria.clicked.connect(self.abrir_galeria)
        btn_galeria.setStyleSheet("padding: 8px; font-weight: bold;")

        self.btn_whatsapp = QPushButton("📤 WhatsApp")
        self.btn_whatsapp.setFixedHeight(40)
        self.btn_whatsapp.setToolTip("Enviar imagem via WhatsApp")
        self.btn_whatsapp.clicked.connect(self.enviar_whatsapp)
        self.btn_whatsapp.setStyleSheet(
            "background-color: #25D366; color: black; padding: 10px 16px; border-radius: 8px; font-weight: bold;"
        )
        self.btn_whatsapp.setVisible(self.config.get("whatsapp", {}).get("ativo", False))

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        top_bar.addWidget(btn_voltar)
        top_bar.addWidget(btn_config)
        top_bar.addWidget(btn_galeria)
        top_bar.addItem(spacer)
        top_bar.addWidget(self.btn_whatsapp)

        self.main_layout.addLayout(top_bar)

    def create_image_area(self):
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(500)
        self.image_label.setStyleSheet("border: 2px solid #444; margin: 10px;")
        self.main_layout.addWidget(self.image_label)

    def create_thumbnail_area(self):
        self.thumbnail_layout = QHBoxLayout()
        self.thumbnail_widgets = []
        self.thumbnail_container = QWidget()
        self.thumbnail_container.setLayout(self.thumbnail_layout)
        self.main_layout.addWidget(self.thumbnail_container)

    def check_for_new_images(self):
        if not os.path.exists(self.fotos_path):
            return

        valid_files = [f for f in os.listdir(self.fotos_path)
                       if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        full_paths = [os.path.join(self.fotos_path, f) for f in sorted(valid_files, reverse=True)]

        if full_paths != self.image_paths:
            self.image_paths = full_paths
            self.update_gallery()

    def update_gallery(self):
        for i in reversed(range(self.thumbnail_layout.count())):
            self.thumbnail_layout.itemAt(i).widget().setParent(None)

        self.thumbnail_widgets.clear()

        for path in self.image_paths[:4]:
            thumbnail = QLabel()
            thumbnail.setPixmap(QPixmap(path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            thumbnail.setStyleSheet("border: 2px solid white; margin: 6px;")
            thumbnail.setCursor(Qt.CursorShape.PointingHandCursor)
            thumbnail.mousePressEvent = lambda e, p=path: self.display_image(p)
            self.thumbnail_layout.addWidget(thumbnail)
            self.thumbnail_widgets.append(thumbnail)

        if self.image_paths:
            self.display_image(self.image_paths[0])

    def display_image(self, path):
        self.current_image_path = path
        pixmap = QPixmap(path).scaled(900, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.repaint()

    def enviar_whatsapp(self):
        if self.current_image_path:
            self.whatsapp.enviar(self.current_image_path)

    def abrir_configuracoes(self):
        self.config_window = ConfigWindow()
        self.config_window.show()

    def abrir_galeria(self):
        self.slideshow_window = SlideshowWindow(self.image_paths)
        self.slideshow_window.show()

    def voltar_para_eventos(self):
        from src.ui.event_window import EventWindow
        self.hide()
        self.event_window = EventWindow()
        self.event_window.show()
