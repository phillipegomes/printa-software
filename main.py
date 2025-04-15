
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.event_window import EventWindow

def main():
    app = QApplication(sys.argv)
    window = EventWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
