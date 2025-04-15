
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QAbstractItemView, QHeaderView
)
from PyQt6.QtCore import Qt
import os
import shutil
from datetime import datetime
from src.ui.main_window import MainWindow

class EventWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print A – Eventos")
        self.setGeometry(200, 100, 900, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #f2f2f2;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                font-size: 15px;
            }
            QPushButton {
                background-color: #1f1f1f;
                color: white;
                border: 1px solid #2d2d2d;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #3a3a3c;
                border-radius: 6px;
                padding: 10px;
                color: white;
            }
            QHeaderView::section {
                background-color: #181818;
                padding: 8px;
                font-weight: bold;
                color: #d0d0d0;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #2c2c2c;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("Meus Eventos")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome do Evento", "Data", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.cellDoubleClicked.connect(self.abrir_evento_duplo_clique)
        layout.addWidget(self.table)

        self.carregar_eventos_existentes()

        layout.addSpacing(20)

        form_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Nome do novo evento...")
        form_layout.addWidget(self.input)

        btn_criar = QPushButton("🟢 Criar Evento")
        btn_criar.clicked.connect(self.criar_evento)
        form_layout.addWidget(btn_criar)

        btn_duplicar = QPushButton("📄 Duplicar Evento Selecionado")
        btn_duplicar.clicked.connect(self.duplicar_evento_selecionado)
        form_layout.addWidget(btn_duplicar)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def carregar_eventos_existentes(self):
        self.table.setRowCount(0)
        eventos_path = "eventos"
        if not os.path.exists(eventos_path):
            os.makedirs(eventos_path)

        eventos = sorted(os.listdir(eventos_path), reverse=True)
        for idx, nome in enumerate(eventos):
            caminho = os.path.join(eventos_path, nome)
            if os.path.isdir(caminho) and nome != "default_config.json":
                data_mod = datetime.fromtimestamp(os.path.getmtime(caminho)).strftime("%d/%m/%Y")
                self.table.insertRow(idx)
                self.table.setItem(idx, 0, QTableWidgetItem(nome))
                self.table.setItem(idx, 1, QTableWidgetItem(data_mod))

                btn_excluir = QPushButton("✖")
                btn_excluir.setStyleSheet("color: #ff453a; font-size: 16px; margin-right: 4px;")
                btn_excluir.setToolTip("Excluir Evento")
                btn_excluir.clicked.connect(lambda _, p=caminho: self.excluir_evento(p))

                layout_btn = QHBoxLayout()
                layout_btn.addWidget(btn_excluir)
                layout_btn.setAlignment(Qt.AlignmentFlag.AlignRight)
                layout_btn.setContentsMargins(0, 0, 0, 0)

                widget = QWidget()
                widget.setLayout(layout_btn)
                self.table.setCellWidget(idx, 2, widget)

    def criar_evento(self):
        nome = self.input.text().strip()
        if not nome:
            QMessageBox.warning(self, "Erro", "Digite um nome para o evento.")
            return
        caminho = os.path.join("eventos", nome)
        if os.path.exists(caminho):
            QMessageBox.warning(self, "Erro", "Esse evento já existe.")
            return
        os.makedirs(caminho)
        os.makedirs(os.path.join(caminho, "Fotos"))
        default_config = os.path.join("eventos", "default_config.json")
        if os.path.exists(default_config):
            shutil.copy(default_config, os.path.join(caminho, "config.json"))
        self.abrir_main(caminho)

    def duplicar_evento_selecionado(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Aviso", "Selecione um evento para duplicar.")
            return
        nome_origem = self.table.item(selected, 0).text()
        pasta_origem = os.path.join("eventos", nome_origem)

        base_nome = nome_origem + "_Copia"
        count = 1
        while os.path.exists(os.path.join("eventos", f"{base_nome}_{count}")):
            count += 1
        novo_nome = f"{base_nome}_{count}"
        destino = os.path.join("eventos", novo_nome)
        shutil.copytree(pasta_origem, destino)
        self.carregar_eventos_existentes()

    def abrir_evento_duplo_clique(self, row, column):
        nome = self.table.item(row, 0).text()
        caminho = os.path.join("eventos", nome)
        self.abrir_main(caminho)

    def abrir_main(self, caminho_evento):
        self.hide()
        self.main = MainWindow(evento_path=caminho_evento)
        self.main.show()

    def excluir_evento(self, caminho_evento):
        nome = os.path.basename(caminho_evento)
        confirmar = QMessageBox.question(self, "Excluir Evento", f"Tem certeza que deseja excluir o evento '{nome}'?")
        if confirmar == QMessageBox.StandardButton.Yes:
            shutil.rmtree(caminho_evento)
            self.carregar_eventos_existentes()
