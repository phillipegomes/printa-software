class PrinterManager:
    def __init__(self, evento_path, config):
        self.evento_path = evento_path
        self.config = config
        self.status = "Pronto"
        self.total_impressoes = 0
        self.fotos_restantes = 999

    def imprimir(self, imagem_path, copias=1):
        print(f"🖨️ Imprimindo {copias}x: {imagem_path}")
        self.total_impressoes += copias