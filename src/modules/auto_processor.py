import os
import shutil
from PIL import Image
from src.modules.ai_processor import apply_ai_filter
from src.modules.layout_applier import apply_layout
from src.modules.qr_smugmug import QRSmugMugUploader
from src.modules.whatsapp_sender import WhatsAppSender
from src.modules.printer_manager import PrinterManager

class AutoProcessor:
    def __init__(self, config):
        self.config = config
        self.uploader = QRSmugMugUploader()
        self.whats = WhatsAppSender()
        self.printer = PrinterManager()
        self.event_path = config.event_folder
        self.input_path = os.path.join(self.event_path, "Fotos")
        self.output_path = os.path.join(self.event_path, "Impressas")
        os.makedirs(self.output_path, exist_ok=True)

    def process_image(self, image_path):
        filename = os.path.basename(image_path)
        original = image_path

        print(f"📥 Imagem recebida: {filename}")

        # IA
        if self.config.config["ia_ativa"]:
            image_path = apply_ai_filter(image_path)
            print(f"🤖 IA aplicada: {image_path}")

        # Layout
        layout_path = self.config.config["layout_path"]
        if layout_path and os.path.exists(layout_path):
            image_path = apply_layout(image_path, layout_path)
            print(f"🎨 Layout aplicado: {image_path}")

        # Salvar imagem final
        final_path = os.path.join(self.output_path, os.path.basename(image_path))
        shutil.copy(image_path, final_path)
        print(f"💾 Imagem final salva: {final_path}")

        # Impressão
        if self.config.config["auto_print"]:
            self.printer.imprimir(final_path)
            print(f"🖨️ Imprimindo imagem: {final_path}")

        # QR + SmugMug
        if self.config.config["qr_ativo"]:
            qr_path = self.uploader.gerar_qr(final_path)
            self.uploader.enviar_smugmug(final_path)
            print(f"🔗 QR + SmugMug enviados")

        # WhatsApp
        if self.config.config["whatsapp_ativo"]:
            self.whats.enviar(final_path)
            print(f"📤 Envio via WhatsApp realizado")

        return final_path
