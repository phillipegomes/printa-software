# src/ui/main_actions.py

import os
import subprocess
from PIL import Image
from PyQt6.QtWidgets import QMessageBox

def carregar_imagens(pasta_fotos):
    if not os.path.exists(pasta_fotos):
        return []
    return sorted([
        os.path.join(pasta_fotos, f)
        for f in os.listdir(pasta_fotos)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ], key=os.path.getmtime)

def imprimir_imagem(path):
    try:
        if os.name == "posix":
            subprocess.run(["lp", path], check=True)
        elif os.name == "nt":
            os.startfile(path, "print")
        else:
            raise OSError("Sistema operacional não suportado para impressão.")
    except Exception as e:
        QMessageBox.critical(None, "Erro ao Imprimir", str(e))

def enviar_whatsapp(path):
    try:
        # Simulação de envio
        QMessageBox.information(None, "WhatsApp", f"Imagem '{os.path.basename(path)}' enviada via WhatsApp!")
    except Exception as e:
        QMessageBox.critical(None, "Erro no WhatsApp", str(e))

def excluir_imagem(path):
    try:
        os.remove(path)
    except Exception as e:
        QMessageBox.critical(None, "Erro ao Excluir", str(e))
