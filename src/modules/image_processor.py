# src/modules/image_processor.py

import os
from PIL import Image
from src.modules.printer_manager import PrinterManager
from src.modules.whatsapp_sender import WhatsAppSender

class ImageProcessor:
    def __init__(self, evento_path, config_manager):
        self.evento_path = evento_path
        self.config_manager = config_manager
        self.config = self.config_manager.config

        self.printer = PrinterManager(
            self.evento_path,
            self.config.get("impressao", {})
        )

        self.whatsapp = WhatsAppSender(
            self.config.get("compartilhamento", {}).get("whatsapp", {})
        )

        # Define pastas
        self.fotos_path = os.path.join(evento_path, "Fotos")
        self.impressas_path = os.path.join(evento_path, "Impressas")
        os.makedirs(self.fotos_path, exist_ok=True)
        os.makedirs(self.impressas_path, exist_ok=True)

    def imprimir(self, imagem_path, copias=1):
        if not os.path.exists(imagem_path):
            print("❌ Imagem não encontrada para imprimir:", imagem_path)
            return

        self.printer.imprimir(imagem_path, copias)

    def enviar_whatsapp(self, imagem_path):
        self.whatsapp.enviar(imagem_path)
