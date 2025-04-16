# src/ui/config_window.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTabWidget, QHBoxLayout,
    QMessageBox
)
from src.ui.compartilhamento_config import CompartilhamentoConfig
from src.ui.ia_config import IAConfig
from src.ui.layout_editor import LayoutEditor
from src.ui.relatorio_window import RelatorioWindow
from src.modules.config_manager import ConfigManager
import os

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurações - Print A")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #202020; color: white; font-family: Arial;")

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 10px; }")

        self.config_path = os.path.join("config", "settings.json")
        self.config_manager = ConfigManager(self.config_path)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)

        self.adicionar_abas()
        self.adicionar_botoes()

    def adicionar_abas(self):
        self.tab_ia = IAConfig(self.config_manager)
        self.tab_compartilhamento = CompartilhamentoConfig(self.config_manager)
        self.tab_layout = LayoutEditor(self.config_manager)
        self.tab_relatorio = RelatorioWindow(self.config_manager)

        self.tabs.addTab(self.tab_layout, "🖼 Layout")
        self.tabs.addTab(self.tab_compartilhamento, "📤 Compartilhar")
        self.tabs.addTab(self.tab_ia, "🧠 IA")
        self.tabs.addTab(self.tab_relatorio, "📊 Relatórios")

    def adicionar_botoes(self):
        button_layout = QHBoxLayout()

        self.btn_salvar = QPushButton("💾 Salvar")
        self.btn_salvar.clicked.connect(self.salvar_tudo)

        self.btn_reverter = QPushButton("↩ Reverter para padrão")
        self.btn_reverter.clicked.connect(self.reverter_padrao)

        button_layout.addStretch()
        button_layout.addWidget(self.btn_salvar)
        button_layout.addWidget(self.btn_reverter)

        self.layout.addLayout(button_layout)

    def salvar_tudo(self):
        self.tab_ia.salvar()
        self.tab_compartilhamento.salvar()
        self.tab_layout.salvar()
        self.tab_relatorio.salvar()
        self.config_manager.salvar_config()
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")

    def reverter_padrao(self):
        confirmar = QMessageBox.question(self, "Confirmar",
            "Deseja realmente reverter todas as configurações para o padrão?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmar == QMessageBox.StandardButton.Yes:
            self.config_manager.reverter_para_padrao()
            self.close()
