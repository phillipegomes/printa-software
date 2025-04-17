from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from src.modules.report_manager import ReportManager

class RelatorioWindow(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.setWindowTitle("Relatórios - Print A")
        self.setGeometry(200, 200, 500, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")

        self.config_manager = config_manager  # Pode ser usado no futuro
        self.manager = ReportManager()

        self.layout = QVBoxLayout()
        self.label = QLabel("Resumo do Evento")
        self.label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.label)

        self.resumo = QTextEdit()
        self.resumo.setStyleSheet("background-color: #2e2e2e; color: white;")
        self.resumo.setReadOnly(True)
        self.layout.addWidget(self.resumo)

        self.btn_csv = QPushButton("📄 Exportar CSV")
        self.btn_csv.clicked.connect(self.exportar_csv)
        self.layout.addWidget(self.btn_csv)

        self.btn_pdf = QPushButton("🧾 Exportar PDF")
        self.btn_pdf.clicked.connect(self.exportar_pdf)
        self.layout.addWidget(self.btn_pdf)

        self.setLayout(self.layout)
        self.atualizar_resumo()

    def atualizar_resumo(self):
        texto = ""
        for k, v in self.manager.data.items():
            if k != "erros":
                texto += f"{k.capitalize()}: {v}\n"
        if self.manager.data.get("erros"):
            texto += "\nErros:\n"
            for erro in self.manager.data["erros"]:
                texto += f"- {erro['hora']}: {erro['erro']}\n"
        self.resumo.setPlainText(texto)

    def exportar_csv(self):
        caminho = self.manager.exportar_csv()
        self.resumo.append(f"\nCSV exportado para: {caminho}")

    def exportar_pdf(self):
        caminho = self.manager.exportar_pdf()
        self.resumo.append(f"\nPDF exportado para: {caminho}")
