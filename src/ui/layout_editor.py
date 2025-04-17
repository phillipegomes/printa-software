# src/ui/layout_editor.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsItem
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import Qt, QPointF

class LayoutEditor(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.config = self.config_manager.config.setdefault("layout", {})

        self.setWindowTitle("Editor de Layout - Print A")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.top_bar = QHBoxLayout()
        self.layout.addLayout(self.top_bar)

        self.btn_add_foto = QPushButton("📸 Adicionar Foto")
        self.btn_add_foto.setStyleSheet("background-color: #444; color: white; padding: 8px;")
        self.btn_add_foto.clicked.connect(self.add_foto)
        self.top_bar.addWidget(self.btn_add_foto)

        self.btn_add_texto = QPushButton("🔤 Adicionar Texto")
        self.btn_add_texto.setStyleSheet("background-color: #444; color: white; padding: 8px;")
        self.btn_add_texto.clicked.connect(self.add_texto)
        self.top_bar.addWidget(self.btn_add_texto)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setStyleSheet("background-color: white;")
        self.layout.addWidget(self.view)

        self.setAcceptDrops(True)

        # Botões de controle
        self.footer = QHBoxLayout()
        self.btn_salvar = QPushButton("💾 Salvar Layout")
        self.btn_salvar.clicked.connect(self.salvar)

        self.btn_reverter = QPushButton("↩ Reverter para padrão")
        self.btn_reverter.clicked.connect(self.reverter_padrao)

        self.footer.addWidget(self.btn_salvar)
        self.footer.addWidget(self.btn_reverter)
        self.layout.addLayout(self.footer)

    def add_foto(self):
        file, _ = QFileDialog.getOpenFileName(self, "Escolha uma imagem", "", "Imagens (*.png *.jpg *.jpeg)")
        if file:
            pixmap = QPixmap(file).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
            item = QGraphicsPixmapItem(pixmap)
            item.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            self.scene.addItem(item)

    def add_texto(self):
        texto = QGraphicsTextItem("Texto Exemplo")
        texto.setFont(QFont("Arial", 18))
        texto.setDefaultTextColor(QColor("black"))
        texto.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        texto.setPos(QPointF(100, 100))
        self.scene.addItem(texto)

    def salvar(self):
        # Aqui poderia ser adicionado salvamento do layout, posições, etc.
        self.config_manager.salvar_config()

    def reverter_padrao(self):
        self.scene.clear()
