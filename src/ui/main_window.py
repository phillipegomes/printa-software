# src/ui/main_window.py

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from src.ui.main_styles import MAIN_STYLE, THUMB_STYLE, BUTTON_STYLE, FLOATING_BUTTON_STYLE
from src.ui.main_actions import carregar_imagens, imprimir_imagem, excluir_imagem, enviar_whatsapp

class MainWindow(QWidget):
    def __init__(self, evento_path, controller=None):
        super().__init__()
        self.evento_path = evento_path
        self.controller = controller
        self.fotos_path = os.path.join(evento_path, "Fotos")
        self.imagens = []
        self.imagem_atual = None

        self.setWindowTitle(os.path.basename(evento_path) + " - Print A")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MAIN_STYLE)

        layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        self.btn_voltar = QPushButton("← Voltar")
        self.btn_voltar.setStyleSheet(BUTTON_STYLE)
        self.btn_voltar.clicked.connect(self.voltar)
        top_bar.addWidget(self.btn_voltar)

        top_bar.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.btn_config = QPushButton("⚙️ Configurações")
        self.btn_config.setStyleSheet(BUTTON_STYLE)
        self.btn_config.clicked.connect(self.abrir_configuracoes)
        top_bar.addWidget(self.btn_config)

        layout.addLayout(top_bar)

        self.label_imagem = QLabel("Nenhuma imagem selecionada")
        self.label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_imagem.setStyleSheet("font-size: 18px; padding: 20px;")
        layout.addWidget(self.label_imagem, stretch=1)

        self.actions_layout = QHBoxLayout()
        self.actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(self.actions_layout)

        self.area_thumbs = QScrollArea()
        self.area_thumbs.setWidgetResizable(True)
        self.area_thumbs.setFixedHeight(200)
        self.area_thumbs.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.area_thumbs.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container_thumbs = QFrame()
        self.thumbs_layout = QHBoxLayout()
        self.thumbs_layout.setSpacing(10)
        self.container_thumbs.setLayout(self.thumbs_layout)
        self.area_thumbs.setWidget(self.container_thumbs)

        layout.addWidget(self.area_thumbs)
        self.setLayout(layout)

        self.carregar()

    def carregar(self):
        self.imagens = carregar_imagens(self.fotos_path)
        self.thumbs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.thumbs_layout.setContentsMargins(10, 0, 10, 0)
        self.thumbs_layout.setSpacing(10)

        for imagem in self.imagens[-4:]:
            thumb_frame = QFrame()
            thumb_frame.setFixedSize(160, 180)
            thumb_frame.setStyleSheet(THUMB_STYLE)

            thumb_layout = QVBoxLayout()
            thumb_layout.setContentsMargins(0, 0, 0, 0)
            thumb_layout.setSpacing(4)

            img_label = QLabel()
            img_label.setPixmap(QPixmap(imagem).scaledToHeight(140))
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.mousePressEvent = lambda e, img=imagem: self.mostrar_imagem(img)
            thumb_layout.addWidget(img_label)

            thumb_frame.setLayout(thumb_layout)
            self.thumbs_layout.addWidget(thumb_frame)

        if self.imagens:
            self.mostrar_imagem(self.imagens[-1])

    def mostrar_imagem(self, path):
        self.imagem_atual = path
        pixmap = QPixmap(path).scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_imagem.setPixmap(pixmap)

        # Remove botões antigos
        for i in reversed(range(self.actions_layout.count())):
            widget = self.actions_layout.itemAt(i).widget()
            if widget:
                self.actions_layout.removeWidget(widget)
                widget.deleteLater()

        # Adiciona os botões na imagem principal
        btn_print = QPushButton("🖨️")
        btn_print.setStyleSheet(FLOATING_BUTTON_STYLE)
        btn_print.clicked.connect(lambda: imprimir_imagem(path))

        btn_whatsapp = QPushButton("💬")
        btn_whatsapp.setStyleSheet(FLOATING_BUTTON_STYLE)
        btn_whatsapp.clicked.connect(lambda: enviar_whatsapp(path))

        btn_delete = QPushButton("❌")
        btn_delete.setStyleSheet(FLOATING_BUTTON_STYLE)
        btn_delete.clicked.connect(lambda: self.confirmar_exclusao(path))

        self.actions_layout.addWidget(btn_print)
        self.actions_layout.addWidget(btn_whatsapp)
        self.actions_layout.addWidget(btn_delete)

    def confirmar_exclusao(self, path):
        resp = QMessageBox.question(self, "Excluir Imagem", "Tem certeza que deseja excluir essa imagem?")
        if resp == QMessageBox.StandardButton.Yes:
            excluir_imagem(path)
            self.carregar()

    def voltar(self):
        if self.controller:
            self.controller.open_event_window()

    def abrir_configuracoes(self):
        if self.controller:
            self.controller.open_config_window()
