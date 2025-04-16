import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QMessageBox, QStackedLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from src.ui.main_styles import MAIN_STYLE, THUMB_STYLE, BUTTON_STYLE, FLOATING_BUTTON_STYLE
from src.ui.main_actions import carregar_imagens, imprimir_imagem, excluir_imagem, enviar_whatsapp

class MainWindow(QWidget):
    def __init__(self, evento_path):
        super().__init__()
        self.evento_path = evento_path
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
        self.btn_voltar.clicked.connect(self.fechar_janela)
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

        # Carregar as miniaturas limitadas a 4 imagens visíveis
        for imagem in self.imagens[:4]:
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

            # Botões de ação flutuantes (só nas miniaturas)
            actions_layout = QHBoxLayout()
            btn_print = QPushButton("🖨️")
            btn_print.setStyleSheet(FLOATING_BUTTON_STYLE)
            btn_print.clicked.connect(lambda _, path=imagem: imprimir_imagem(path))

            btn_whatsapp = QPushButton("💬")
            btn_whatsapp.setStyleSheet(FLOATING_BUTTON_STYLE)
            btn_whatsapp.clicked.connect(lambda _, path=imagem: enviar_whatsapp(path))

            btn_delete = QPushButton("❌")
            btn_delete.setStyleSheet(FLOATING_BUTTON_STYLE)
            btn_delete.clicked.connect(lambda _, path=imagem: excluir_imagem(path))

            actions_layout.addWidget(btn_print)
            actions_layout.addWidget(btn_whatsapp)
            actions_layout.addWidget(btn_delete)

            thumb_layout.addLayout(actions_layout)
            thumb_frame.setLayout(thumb_layout)

            self.thumbs_layout.addWidget(thumb_frame)

        # Exibir a última foto como foto principal
        if self.imagens:
            self.mostrar_imagem(self.imagens[-1])

    def mostrar_imagem(self, path):
        self.imagem_atual = path
        pixmap = QPixmap(path).scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_imagem.setPixmap(pixmap)

    def fechar_janela(self):
        self.close()  # Fechar a janela atual, mas pode ser adaptado para voltar

    def abrir_configuracoes(self):
        print("Abrindo configurações...")  # Simulação de ação
