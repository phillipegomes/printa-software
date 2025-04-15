# src/ui/config_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from src.ui.ia_config import IAConfigWindow
from src.ui.compartilhamento_config import CompartilhamentoConfig

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurações do Sistema")
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        # Botão IA
        btn_ia = QPushButton("🎨 Configurar IA")
        btn_ia.setStyleSheet("background-color: #444; padding: 10px; margin: 5px;")
        btn_ia.clicked.connect(self.abrir_config_ia)
        layout.addWidget(btn_ia)

        # Botão Compartilhamento
        btn_comp = QPushButton("📤 Compartilhamento")
        btn_comp.setStyleSheet("background-color: #444; padding: 10px; margin: 5px;")
        btn_comp.clicked.connect(self.abrir_config_compartilhamento)
        layout.addWidget(btn_comp)

        # Botões Placeholder para futuras abas
        btn_impressao = QPushButton("🖨 Impressão")
        btn_impressao.setStyleSheet("background-color: #333; padding: 10px; margin: 5px;")
        btn_impressao.setEnabled(False)
        layout.addWidget(btn_impressao)

        btn_layout = QPushButton("🧩 Layout")
        btn_layout.setStyleSheet("background-color: #333; padding: 10px; margin: 5px;")
        btn_layout.setEnabled(False)
        layout.addWidget(btn_layout)

        btn_relatorio = QPushButton("📊 Relatórios")
        btn_relatorio.setStyleSheet("background-color: #333; padding: 10px; margin: 5px;")
        btn_relatorio.setEnabled(False)
        layout.addWidget(btn_relatorio)

        self.setLayout(layout)

    def abrir_config_ia(self):
        self.ia_win = IAConfigWindow()
        self.ia_win.show()

    def abrir_config_compartilhamento(self):
        self.compart_win = CompartilhamentoConfig()
        self.compart_win.show()
