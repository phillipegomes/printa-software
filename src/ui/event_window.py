
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QSpacerItem, QSizePolicy, QFrame, QInputDialog, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QPoint
from datetime import datetime  # ADICIONADO: Importação do datetime
from src.ui.main_window import MainWindow
from src.ui.event_actions import criar_evento, duplicar_evento, renomear_evento, excluir_evento
from src.ui.event_styles import TABELA_STYLE, BOTAO_STYLE, INPUT_STYLE, MENU_STYLE

class EventWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print A – Meus Eventos")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.eventos_path = "eventos"
        os.makedirs(self.eventos_path, exist_ok=True)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Meus Eventos")
        titulo.setStyleSheet("font-size: 24px; font-weight: 600; margin: 10px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(["Nome", "Data", "Excluir"])
        self.tabela.setColumnWidth(1, 120)
        self.tabela.setColumnWidth(2, 70)
        self.tabela.horizontalHeader().setStretchLastSection(False)
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.setStyleSheet(TABELA_STYLE)
        self.tabela.cellClicked.connect(self.selecionar_evento)
        self.tabela.cellDoubleClicked.connect(self.abrir_evento)
        self.tabela.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabela.customContextMenuRequested.connect(self.abrir_menu_contexto)
        layout.addWidget(self.tabela)

        layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        input_frame = QFrame()
        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Digite o nome do novo evento...")
        self.input_nome.setStyleSheet(INPUT_STYLE)
        input_layout.addWidget(self.input_nome)

        self.btn_criar = QPushButton("Criar Evento")
        self.btn_criar.setStyleSheet(BOTAO_STYLE)
        self.btn_criar.clicked.connect(self.criar_evento_click)
        input_layout.addWidget(self.btn_criar)

        self.btn_abrir = QPushButton("Abrir Evento")
        self.btn_abrir.setEnabled(False)
        self.btn_abrir.setStyleSheet(BOTAO_STYLE)
        self.btn_abrir.clicked.connect(self.abrir_evento)
        input_layout.addWidget(self.btn_abrir)

        self.btn_duplicar = QPushButton("Duplicar Evento")
        self.btn_duplicar.setEnabled(False)
        self.btn_duplicar.setStyleSheet(BOTAO_STYLE)
        self.btn_duplicar.clicked.connect(self.duplicar_evento_click)
        input_layout.addWidget(self.btn_duplicar)

        self.btn_renomear = QPushButton("Renomear")
        self.btn_renomear.setEnabled(False)
        self.btn_renomear.setStyleSheet(BOTAO_STYLE)
        self.btn_renomear.clicked.connect(self.renomear_evento_click)
        input_layout.addWidget(self.btn_renomear)

        layout.addWidget(input_frame)
        self.setLayout(layout)

        self.evento_selecionado = None
        self.carregar_eventos()

    def carregar_eventos(self):
        self.tabela.setRowCount(0)
        for nome in sorted(os.listdir(self.eventos_path)):
            caminho = os.path.join(self.eventos_path, nome)
            if os.path.isdir(caminho) and not nome.startswith("."):
                data = datetime.fromtimestamp(os.path.getmtime(caminho)).strftime("%d/%m/%Y")
                row = self.tabela.rowCount()
                self.tabela.insertRow(row)
                self.tabela.setItem(row, 0, QTableWidgetItem(nome))
                self.tabela.setItem(row, 1, QTableWidgetItem(data))

                btn_excluir = QPushButton("❌")
                btn_excluir.setStyleSheet("color: #ff4d4f; font-weight: bold; border: none; background: none;")
                btn_excluir.clicked.connect(lambda _, n=nome: self.excluir_evento_click(n))
                cell_widget = QWidget()
                layout_btn = QHBoxLayout(cell_widget)
                layout_btn.addWidget(btn_excluir)
                layout_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout_btn.setContentsMargins(0, 0, 0, 0)
                self.tabela.setCellWidget(row, 2, cell_widget)

    def selecionar_evento(self, row, column):
        if column != 2:
            self.evento_selecionado = self.tabela.item(row, 0).text()
            self.btn_abrir.setEnabled(True)
            self.btn_duplicar.setEnabled(True)
            self.btn_renomear.setEnabled(True)

    def criar_evento_click(self):
        nome = self.input_nome.text().strip()
        if criar_evento(nome, self.eventos_path):
            self.carregar_eventos()
            self.input_nome.clear()

    def abrir_evento(self):
        if not self.evento_selecionado:
            return
        evento_path = os.path.join(self.eventos_path, self.evento_selecionado)
        self.main_window = MainWindow(evento_path)
        self.main_window.show()
        self.close()

    def duplicar_evento_click(self):
        if duplicar_evento(self.evento_selecionado, self.eventos_path):
            self.carregar_eventos()

    def renomear_evento_click(self):
        if not self.evento_selecionado:
            return
        novo_nome, ok = QInputDialog.getText(self, "Renomear Evento", "Novo nome:", text=self.evento_selecionado)
        if ok and novo_nome.strip():
            if renomear_evento(self.evento_selecionado, novo_nome.strip(), self.eventos_path):
                self.carregar_eventos()

    def excluir_evento_click(self, nome):
        if excluir_evento(nome, self.eventos_path):
            self.carregar_eventos()

    def abrir_menu_contexto(self, pos: QPoint):
        index = self.tabela.indexAt(pos)
        if index.isValid():
            row = index.row()
            self.evento_selecionado = self.tabela.item(row, 0).text()

            menu = QMenu(self)
            menu.setStyleSheet(MENU_STYLE)
            menu.addAction("Abrir Evento", self.abrir_evento)
            menu.addAction("Duplicar Evento", self.duplicar_evento_click)
            menu.addAction("Renomear Evento", self.renomear_evento_click)
            menu.addAction("Excluir Evento", lambda: self.excluir_evento_click(self.evento_selecionado))
            menu.exec(self.tabela.mapToGlobal(pos))
