
from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt
import os

class GalleryWindow(QWidget):
    def __init__(self, image_paths, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Galeria – Print A")
        self.setGeometry(200, 100, 1000, 700)
        self.image_paths = image_paths

        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.grid = QGridLayout()
        scroll_content.setLayout(self.grid)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)
        self.setLayout(layout)

        self.populate_grid()

    def populate_grid(self):
        # Limpa a grade antes de adicionar novas imagens
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        row = 0
        col = 0
        for idx, path in enumerate(self.image_paths):
            if not os.path.exists(path):
                continue

            container = QFrame()
            container.setStyleSheet("background-color: #222; border: 1px solid #444; border-radius: 8px;")
            container.setMinimumSize(220, 250)
            container.setMaximumSize(220, 250)
            vbox = QVBoxLayout(container)
            vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

            img_label = QLabel()
            img_label.setPixmap(QPixmap(path).scaled(200, 140, Qt.AspectRatioMode.KeepAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation))
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            img_label.mousePressEvent = lambda e, p=path: self.visualizar_imagem(p)

            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(6)

            btn_imprimir = QPushButton("🖨️")
            btn_imprimir.setToolTip("Imprimir")
            btn_imprimir.setFixedSize(32, 32)
            btn_imprimir.clicked.connect(lambda _, p=path: self.imprimir(p))

            btn_whatsapp = QPushButton("📤")
            btn_whatsapp.setToolTip("WhatsApp")
            btn_whatsapp.setFixedSize(32, 32)
            btn_whatsapp.clicked.connect(lambda _, p=path: self.enviar_whatsapp(p))

            btn_excluir = QPushButton("❌")
            btn_excluir.setToolTip("Excluir")
            btn_excluir.setFixedSize(32, 32)
            btn_excluir.clicked.connect(lambda _, p=path: self.excluir_imagem(p))

            btn_layout.addWidget(btn_imprimir)
            btn_layout.addWidget(btn_whatsapp)
            btn_layout.addWidget(btn_excluir)

            vbox.addWidget(img_label)
            vbox.addLayout(btn_layout)

            self.grid.addWidget(container, row, col)
            col += 1
            if col >= 4:
                row += 1
                col = 0

    def visualizar_imagem(self, path):
        msg = QMessageBox(self)
        msg.setWindowTitle("Visualizar Imagem")
        pixmap = QPixmap(path).scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        label = QLabel()
        label.setPixmap(pixmap)
        msg.layout().addWidget(label)
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        msg.exec()

    def excluir_imagem(self, path):
        confirmar = QMessageBox.question(self, "Excluir", "Deseja realmente excluir esta imagem?")
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path)
                self.image_paths.remove(path)
                self.populate_grid()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao excluir: {e}")

    def imprimir(self, path):
        print(f"[IMPRIMIR] {path}")  # Substituir pela função real de impressão

    def enviar_whatsapp(self, path):
        print(f"[WHATSAPP] {path}")  # Substituir pela função real de envio via WhatsApp
