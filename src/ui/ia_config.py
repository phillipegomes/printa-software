# src/ui/ia_config.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QCheckBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class IAConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração de IA")
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()

        # Ativar IA
        self.checkbox_ia = QCheckBox("Ativar IA")
        layout.addWidget(self.checkbox_ia)

        # Estilos de IA
        layout.addWidget(QLabel("Escolha um estilo de IA:"))
        self.combo_estilo = QComboBox()
        self.combo_estilo.addItems(["Cartoon (Offline)", "Ghibli (Offline)", "Anime (Online)", "Realismo (Online)", "Game Style (Online)"])
        layout.addWidget(self.combo_estilo)

        # Miniatura de exemplo
        self.img_demo = QLabel()
        self.img_demo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_demo)

        # Descrição
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Descreva o que a IA deve gerar (opcional para IA online)")
        layout.addWidget(self.input_desc)

        # Botão de teste IA
        self.btn_teste = QPushButton("Aplicar Teste com Imagem Exemplo")
        self.btn_teste.clicked.connect(self.aplicar_teste)
        layout.addWidget(self.btn_teste)

        # Botões de ação
        botoes_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("Salvar")
        self.btn_reverter = QPushButton("Reverter padrão")
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_reverter)
        layout.addLayout(botoes_layout)

        self.setLayout(layout)

    def aplicar_teste(self):
        estilo = self.combo_estilo.currentText()
        if "Cartoon" in estilo:
            path_img = "assets/test_cartoon.jpg"
        elif "Ghibli" in estilo:
            path_img = "assets/test_ghibli.jpg"
        elif "Anime" in estilo:
            path_img = "assets/test_anime.jpg"
        elif "Game" in estilo:
            path_img = "assets/test_game.jpg"
        else:
            path_img = "assets/test_realismo.jpg"

        if os.path.exists(path_img):
            self.img_demo.setPixmap(QPixmap(path_img).scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio))
