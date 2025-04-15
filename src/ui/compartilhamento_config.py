
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class CompartilhamentoConfig(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Configurações de Compartilhamento"))
        self.setLayout(layout)
