# src/ui/ia_config.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox,
    QPushButton, QHBoxLayout
)

class IAConfig(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.label = QLabel("\u269b\ufe0f Configurações de Inteligência Artificial")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(self.label)

        self.checkbox_ia = QCheckBox("Ativar IA")
        self.layout.addWidget(self.checkbox_ia)

        # Botões Salvar e Reverter
        btn_layout = QHBoxLayout()
        self.btn_salvar = QPushButton("Salvar IA")
        self.btn_salvar.clicked.connect(self.salvar)

        self.btn_reverter = QPushButton("Reverter padrão")
        self.btn_reverter.clicked.connect(self.reverter_padrao)

        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_reverter)
        self.layout.addLayout(btn_layout)

        self.carregar()

    def carregar(self):
        ia_config = self.config_manager.config.get("ia", {})
        self.checkbox_ia.setChecked(ia_config.get("ativar_ia", False))

    def salvar(self):
        self.config_manager.config.setdefault("ia", {})["ativar_ia"] = self.checkbox_ia.isChecked()
        self.config_manager.salvar_config()  # Garante persistência imediata

    def reverter_padrao(self):
        self.checkbox_ia.setChecked(False)
        self.salvar()
