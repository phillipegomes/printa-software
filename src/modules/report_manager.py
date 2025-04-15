import csv
import json
from datetime import datetime
from fpdf import FPDF
import os

class ReportManager:
    def __init__(self):
        self.reset()
        os.makedirs("reports", exist_ok=True)

    def reset(self):
        self.data = {
            "recebidas": 0,
            "impressas": 0,
            "whatsapp": 0,
            "qrcode": 0,
            "pendentes_ia": 0,
            "pendentes_upload": 0,
            "erros": []
        }

    def registrar_recebida(self):
        self.data["recebidas"] += 1

    def registrar_impressao(self):
        self.data["impressas"] += 1

    def registrar_whatsapp(self):
        self.data["whatsapp"] += 1

    def registrar_qrcode(self):
        self.data["qrcode"] += 1

    def adicionar_erro(self, erro):
        self.data["erros"].append({"erro": erro, "hora": datetime.now().isoformat()})

    def adicionar_pendente_ia(self):
        self.data["pendentes_ia"] += 1

    def adicionar_pendente_upload(self):
        self.data["pendentes_upload"] += 1

    def exportar_csv(self):
        caminho = os.path.join("reports", "relatorio.csv")
        with open(caminho, "w", newline="") as f:
            writer = csv.writer(f)
            for chave, valor in self.data.items():
                if chave != "erros":
                    writer.writerow([chave, valor])
            writer.writerow([])
            writer.writerow(["Erros", "Hora"])
            for erro in self.data["erros"]:
                writer.writerow([erro["erro"], erro["hora"]])
        return caminho

    def exportar_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Relatório de Evento", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        for chave, valor in self.data.items():
            if chave != "erros":
                pdf.cell(200, 10, f"{chave.capitalize()}: {valor}", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, "Erros:", ln=True)
        for erro in self.data["erros"]:
            pdf.cell(200, 10, f"{erro['hora']} - {erro['erro']}", ln=True)

        caminho = os.path.join("reports", "relatorio.pdf")
        pdf.output(caminho)
        return caminho
