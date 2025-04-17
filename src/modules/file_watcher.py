import os
import time
import threading

class FileWatcher:
    def __init__(self, pasta_monitorada, callback):
        self.pasta_monitorada = pasta_monitorada
        self.callback = callback
        self._running = True
        self._arquivos_vistos = set(os.listdir(pasta_monitorada))
        self._thread = threading.Thread(target=self._monitorar, daemon=True)
        self._thread.start()

    def _monitorar(self):
        while self._running:
            try:
                arquivos_atuais = set(os.listdir(self.pasta_monitorada))
                novos_arquivos = arquivos_atuais - self._arquivos_vistos
                for arquivo in novos_arquivos:
                    if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        caminho_completo = os.path.join(self.pasta_monitorada, arquivo)
                        self.callback(caminho_completo)
                self._arquivos_vistos = arquivos_atuais
                time.sleep(2)  # verifica a cada 2 segundos
            except Exception as e:
                print(f"[FileWatcher] Erro ao monitorar: {e}")

    def parar(self):
        self._running = False
        self._thread.join()
