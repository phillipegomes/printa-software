import os
from PIL import Image
from src.modules.ai_processor import apply_ai_filter
from src.modules.qr_smugmug import QRSmugMugUploader
from src.modules.whatsapp_sender import WhatsAppSender
from src.modules.layout_applier import apply_layout  # Simulado

class ImageProcessor:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.qr_uploader = QRSmugMugUploader()
        self.whatsapp = WhatsAppSender()

    def process_image(self, path_original):
        try:
            current_path = path_original
            self.logger.info(f"Iniciando processamento: {path_original}")

            # Aplicar IA se ativado
            if self.config["ia_ativa"]:
                self.logger.info("Aplicando IA...")
                current_path = apply_ai_filter(current_path, estilo=self.config["ia_estilo"])

            # Aplicar layout
            if self.config["layout_path"] and os.path.exists(self.config["layout_path"]):
                self.logger.info("Aplicando layout...")
                current_path = apply_layout(current_path, self.config["layout_path"])

            # Salvar em /Impressas
            impressas_dir = os.path.join(self.config["event_folder"], "Impressas")
            os.makedirs(impressas_dir, exist_ok=True)
            nome_final = os.path.basename(current_path)
            destino = os.path.join(impressas_dir, nome_final)
            Image.open(current_path).save(destino)
            self.logger.info(f"Imagem final salva: {destino}")

            # Enviar para impressão automática se ativado
            if self.config["auto_print"]:
                self.logger.info("Enviando para impressão...")
                os.system(f"lp '{destino}'")  # Simples envio no Mac/Linux

            # Enviar para SmugMug + gerar QR
            if self.config["qr_ativo"]:
                self.logger.info("Enviando para SmugMug e gerando QR...")
                self.qr_uploader.gerar_qr(destino)
                self.qr_uploader.enviar_smugmug(destino)

            # Enviar para WhatsApp
            if self.config["whatsapp_ativo"]:
                self.logger.info("Enviando via WhatsApp...")
                self.whatsapp.enviar(destino)

            return destino

        except Exception as e:
            self.logger.error(f"Erro ao processar imagem: {e}")
            return None
