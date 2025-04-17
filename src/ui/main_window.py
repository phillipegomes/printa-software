
# src/ui/main_window.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import os
from src.modules.config_manager import ConfigManager
from src.modules.image_processor import ImageProcessor
from src.modules.file_watcher import FileWatcher
from src.ui.gallery_window import GalleryWindow

class MainWindow(QWidget):
    def __init__(self, evento_path, controller):
        super().__init__()
        self.setWindowTitle("Print A - Evento")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        self.controller = controller
        self.evento_path = evento_path
        self.fotos_path = os.path.join(evento_path, "Fotos")
        os.makedirs(self.fotos_path, exist_ok=True)

        self.config_manager = ConfigManager()
        self.config_manager.carregar_config()
        self.config = self.config_manager.config

        self.processor = ImageProcessor(self.evento_path, self.config_manager)
        self.file_watcher = FileWatcher(self.fotos_path, self.nova_foto_detectada)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Topo
        top_bar = QHBoxLayout()
        self.btn_voltar = QPushButton("⬅ Voltar")
        self.btn_voltar.clicked.connect(self.controller.open_event_window)
        self.btn_voltar.setFixedHeight(40)
        self.btn_voltar.setStyleSheet("background-color: #444; color: white;")

        self.btn_config = QPushButton("⚙ Configurações")
        self.btn_config.clicked.connect(self.abrir_configuracoes)
        self.btn_config.setFixedHeight(40)
        self.btn_config.setStyleSheet("background-color: #444; color: white;")

        top_bar.addWidget(self.btn_voltar)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_config)
        self.layout.addLayout(top_bar)

        # Foto principal
        self.label_foto = QLabel()
        self.label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_foto)

        # Botões de ação
        self.botoes_acao = QHBoxLayout()
        self.botoes_acao.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_imprimir = QPushButton("🖨️ 1x")
        self.btn_imprimir.setFixedSize(80, 35)
        self.btn_imprimir.clicked.connect(self.imprimir_foto)

        self.btn_whats = QPushButton("📤")
        self.btn_whats.setFixedSize(50, 35)
        self.btn_whats.setEnabled(self.config.get("compartilhamento", {}).get("whatsapp_ativo", False))
        self.btn_whats.clicked.connect(self.enviar_whatsapp)

        self.btn_excluir = QPushButton("❌")
        self.btn_excluir.setFixedSize(50, 35)
        self.btn_excluir.clicked.connect(self.excluir_foto)

        self.botoes_acao.addWidget(self.btn_imprimir)
        self.botoes_acao.addWidget(self.btn_whats)
        self.botoes_acao.addWidget(self.btn_excluir)

        self.layout.addLayout(self.botoes_acao)

        # Miniaturas
        self.thumbnail_bar = QHBoxLayout()
        self.thumbnail_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.thumbnail_bar)

        self.foto_atual = None
        self.atualizar_miniaturas()

    def nova_foto_detectada(self, caminho):
        self.atualizar_miniaturas()

    def atualizar_miniaturas(self):
        # Limpa miniaturas
        while self.thumbnail_bar.count():
            item = self.thumbnail_bar.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        arquivos = sorted([
            os.path.join(self.fotos_path, f)
            for f in os.listdir(self.fotos_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ], key=os.path.getctime, reverse=True)

        if arquivos:
            self.exibir_foto_principal(arquivos[0])
        else:
            self.label_foto.clear()
            self.foto_atual = None

        for caminho in arquivos[:4]:
            thumb = QLabel()
            pixmap = QPixmap(caminho).scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            thumb.setPixmap(pixmap)
            thumb.setStyleSheet("margin: 8px; border: 2px solid #888;")
            thumb.mousePressEvent = lambda event, f=caminho: self.exibir_foto_principal(f)

            self.thumbnail_bar.addWidget(thumb)

    def exibir_foto_principal(self, caminho):
        pixmap = QPixmap(caminho).scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label_foto.setPixmap(pixmap)
        self.foto_atual = caminho

    def imprimir_foto(self):
        if self.foto_atual:
            self.processor.imprimir(self.foto_atual)

    def enviar_whatsapp(self):
        if self.foto_atual:
            self.processor.enviar_whatsapp(self.foto_atual)

    def excluir_foto(self):
        if self.foto_atual and os.path.exists(self.foto_atual):
            os.remove(self.foto_atual)
            self.foto_atual = None
            self.atualizar_miniaturas()

    def abrir_configuracoes(self):
        self.controller.open_config_window()
