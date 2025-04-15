
import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.event_window import EventWindow
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Caminho default do evento inicial, pode ser substituído ao abrir um evento
    evento_default_path = os.path.join("eventos", "Evento_Teste")
    if not os.path.exists(evento_default_path):
        os.makedirs(os.path.join(evento_default_path, "Fotos"))
        default_config = os.path.join("eventos", "default_config.json")
        if os.path.exists(default_config):
            with open(default_config, "r") as f:
                with open(os.path.join(evento_default_path, "config.json"), "w") as fw:
                    fw.write(f.read())

    window = EventWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
