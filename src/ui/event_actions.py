# src/ui/event_actions.py

import os
import shutil
from PyQt6.QtWidgets import QMessageBox

def criar_evento(nome, base_path):
    if not nome:
        QMessageBox.warning(None, "Erro", "Digite um nome para o evento.")
        return False
    caminho = os.path.join(base_path, nome)
    if os.path.exists(caminho):
        QMessageBox.warning(None, "Erro", "Já existe um evento com esse nome.")
        return False
    os.makedirs(os.path.join(caminho, "Fotos"))
    return True

def duplicar_evento(nome, base_path):
    if not nome:
        return False
    origem = os.path.join(base_path, nome)
    i = 1
    novo_nome = f"{nome}_Copia_{i}"
    while os.path.exists(os.path.join(base_path, novo_nome)):
        i += 1
        novo_nome = f"{nome}_Copia_{i}"
    try:
        shutil.copytree(origem, os.path.join(base_path, novo_nome))
        return True
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao duplicar: {e}")
        return False

def renomear_evento(orig, novo, base_path):
    origem = os.path.join(base_path, orig)
    destino = os.path.join(base_path, novo)
    if os.path.exists(destino):
        QMessageBox.warning(None, "Erro", "Já existe um evento com esse nome.")
        return False
    try:
        os.rename(origem, destino)
        return True
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao renomear: {e}")
        return False

def excluir_evento(nome, base_path):
    caminho = os.path.join(base_path, nome)
    confirm = QMessageBox.question(None, "Excluir Evento", f"Tem certeza que deseja excluir o evento '{nome}'?")
    if confirm != QMessageBox.StandardButton.Yes:
        return False
    try:
        shutil.rmtree(caminho)
        return True
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao excluir evento: {e}")
        return False
