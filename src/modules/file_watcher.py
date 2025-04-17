# src/modules/file_watcher.py

import os
import time
import threading

def iniciar_monitoramento(pasta, callback, intervalo=3):
    def monitorar():
        arquivos_vistos = set(os.listdir(pasta))
        while True:
            time.sleep(intervalo)
            arquivos_atuais = set(os.listdir(pasta))
            novos = arquivos_atuais - arquivos_vistos
            if novos:
                for nome in novos:
                    if nome.lower().endswith((".jpg", ".jpeg", ".png")):
                        callback(os.path.join(pasta, nome))
                arquivos_vistos = arquivos_atuais

    thread = threading.Thread(target=monitorar, daemon=True)
    thread.start()
