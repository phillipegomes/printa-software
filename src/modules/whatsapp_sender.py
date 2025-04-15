
import requests
import os

class WhatsAppSender:
    def __init__(self, config):
        self.ativo = config.get("ativo", False)
        self.numero = config.get("numero", "")
        self.mensagem = config.get("mensagem", "Sua foto está pronta!")

    def enviar(self, imagem_path):
        if not self.ativo:
            print("WhatsApp desativado nas configurações.")
            return
        if not os.path.exists(imagem_path):
            print("Imagem não encontrada:", imagem_path)
            return
        if not self.numero:
            print("Número de WhatsApp não configurado.")
            return

        try:
            url = "http://localhost:21465/send-image"
            files = {'file': open(imagem_path, 'rb')}
            data = {
                "phone": self.numero,
                "caption": self.mensagem
            }
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print("✅ Imagem enviada via WhatsApp com sucesso!")
            else:
                print("❌ Erro ao enviar imagem via WhatsApp:", response.text)
        except Exception as e:
            print("⚠️ Falha no envio via WhatsApp:", str(e))
