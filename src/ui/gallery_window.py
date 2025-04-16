# src/ui/gallery_window.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QScrollArea, QGridLayout, QSpinBox, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import os

class GalleryWindow(QWidget):
    def __init__(self, evento_path, main_window):
        super().__init__()
        self.setWindowTitle("Galeria - Print A")
        self.setGeometry(150, 150, 1100, 800)
        self.setStyleSheet("background-color: #121212; color: white; font-family: Arial;")

        self.evento_path = evento_path
        self.main_window = main_window
        self.image_paths = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        self.grid = QGridLayout()
        content.setLayout(self.grid)
        scroll.setWidget(content)

        self.layout.addWidget(scroll)

        self.load_images()

    def load_images(self):
        folder = os.path.join(self.evento_path, "Fotos")
        self.image_paths = []

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not os.path.exists(folder):
            return

        row, col = 0, 0
        for file in sorted(os.listdir(folder), reverse=True):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(folder, file)
                self.image_paths.append(full_path)
                self.add_image_widget(full_path, row, col)
                col += 1
                if col == 3:
                    col = 0
                    row += 1

    def add_image_widget(self, path, row, col):
        container = QVBoxLayout()
        widget = QWidget()
        widget.setStyleSheet("margin: 10px; padding: 10px; border: 1px solid #333;")

        image_label = QLabel()
        image_label.setPixmap(QPixmap(path).scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_row = QHBoxLayout()

        btn_print = QPushButton("🖨")
        btn_print.setToolTip("Imprimir")
        btn_print.clicked.connect(lambda: self.imprimir(path))

        self.copias_box = QSpinBox()
        self.copias_box.setMinimum(1)
        self.copias_box.setMaximum(self.get_limite_impressoes())
        self.copias_box.setValue(1)
        self.copias_box.setToolTip("Número de cópias")
        self.copias_box.setFixedWidth(60)

        btn_share = QPushButton("📤")
        btn_share.setToolTip("Compartilhar (WhatsApp)")
        btn_share.clicked.connect(lambda: self.compartilhar(path))

        btn_delete = QPushButton("❌")
        btn_delete.setToolTip("Excluir imagem")
        btn_delete.clicked.connect(lambda: self.confirmar_exclusao(path))

        btn_row.addWidget(btn_print)
        btn_row.addWidget(self.copias_box)
        btn_row.addWidget(btn_share)
        btn_row.addWidget(btn_delete)

        container.addWidget(image_label)
        container.addLayout(btn_row)
        widget.setLayout(container)
        self.grid.addWidget(widget, row, col)

    def get_limite_impressoes(self):
        return self.main_window.config.get("impressao", {}).get("max_copias", 5)

    def imprimir(self, path):
        copias = self.copias_box.value()
        print(f"[GALERIA] Enviando para impressão: {path} x{copias}")
        # Aqui entraria a chamada para o gerenciador de impressão

    def compartilhar(self, path):
        if not self.main_window.config.get("whatsapp", {}).get("ativo", False):
            QMessageBox.warning(self, "WhatsApp desativado", "O envio via WhatsApp não está ativado nas configurações.")
            return
        print(f"[GALERIA] Enviando via WhatsApp: {path}")
        self.main_window.whatsapp.enviar(path)

    def confirmar_exclusao(self, path):
        confirmar = QMessageBox.question(self, "Excluir Imagem", f"Deseja realmente excluir esta imagem?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmar == QMessageBox.StandardButton.Yes:
            os.remove(path)
            print(f"[GALERIA] Imagem excluída: {path}")
            self.load_images()
