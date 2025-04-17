from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
import os

class CompartilhamentoConfig(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.config = self.config_manager.config.setdefault("compartilhamento", {})
        layout = QVBoxLayout(self)

        self.checkbox_whatsapp = QCheckBox("Ativar envio por WhatsApp")
        self.input_numero = QLineEdit()
        self.input_mensagem = QLineEdit()
        layout.addWidget(self.checkbox_whatsapp)
        layout.addWidget(self.input_numero)
        layout.addWidget(self.input_mensagem)

        btns = QHBoxLayout()
        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)
        btns.addWidget(self.btn_salvar)
        layout.addLayout(btns)
        self.carregar()

    def carregar(self):
        self.checkbox_whatsapp.setChecked(self.config.get("whatsapp_ativo", False))
        self.input_numero.setText(self.config.get("whatsapp_numero", ""))
        self.input_mensagem.setText(self.config.get("whatsapp_mensagem", ""))

    def salvar(self):
        self.config["whatsapp_ativo"] = self.checkbox_whatsapp.isChecked()
        self.config["whatsapp_numero"] = self.input_numero.text()
        self.config["whatsapp_mensagem"] = self.input_mensagem.text()
        self.config_manager.salvar_config()