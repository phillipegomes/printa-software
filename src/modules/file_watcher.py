import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.modules.config_manager import ConfigManager
from src.modules.auto_processor import AutoProcessor

class FotoHandler(FileSystemEventHandler):
    def __init__(self, processor):
        self.processor = processor

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"📸 Nova imagem detectada: {event.src_path}")
            time.sleep(1)  # aguarda escrita completa
            try:
                self.processor.process_image(event.src_path)
            except Exception as e:
                print(f"❌ Erro ao processar imagem: {e}")

def iniciar_monitoramento():
    config = ConfigManager("eventos/Evento_Teste")
    processor = AutoProcessor(config)
    path = os.path.join(config.event_folder, "Fotos")

    os.makedirs(path, exist_ok=True)

    event_handler = FotoHandler(processor)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print(f"📂 Monitorando pasta: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    iniciar_monitoramento()
