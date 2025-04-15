import qrcode
import os
import time

class QRSmugMugUploader:
    def __init__(self):
        self.base_url = "https://smugmug.com/evento123"  # URL base simulada
        self.pendentes = []

    def gerar_qr(self, imagem_path):
        nome_arquivo = os.path.basename(imagem_path)
        url = f"{self.base_url}/{nome_arquivo}"
        qr_path = imagem_path.replace(".", "_qrcode.")
        try:
            qr = qrcode.make(url)
            qr.save(qr_path)
            print("QR Code gerado:", qr_path)
            return qr_path
        except Exception as e:
            print("Erro ao gerar QR:", e)
            return None

    def enviar_smugmug(self, imagem_path):
        try:
            print("Simulando envio para SmugMug:", imagem_path)
            time.sleep(1)
        except Exception as e:
            print("Erro ao enviar:", e)
            self.pendentes.append(imagem_path)

    def reenviar_pendentes(self):
        for img in self.pendentes:
            self.enviar_smugmug(img)
        self.pendentes.clear()
