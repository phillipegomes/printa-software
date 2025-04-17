# src/controller/app_controller.py

from PyQt6.QtWidgets import QApplication
from src.ui.event_window import EventWindow
from src.ui.main_window import MainWindow
from src.ui.config_window import ConfigWindow
from src.ui.gallery_window import GalleryWindow

class AppController:
    def __init__(self):
        self.app = QApplication([])
        self.current_window = None
        self.evento_path = None

    def start(self):
        self.open_event_window()
        self.app.exec()

    def open_event_window(self):
        self.close_current_window()
        self.current_window = EventWindow(controller=self)
        self.current_window.show()

    def open_main_window(self, evento_path):
        self.close_current_window()
        self.evento_path = evento_path
        self.current_window = MainWindow(evento_path, controller=self)
        self.current_window.show()

    def open_config_window(self):
        self.close_current_window()
        self.current_window = ConfigWindow()
        self.current_window.show()

    def open_gallery_window(self):
        if self.evento_path:
            self.close_current_window()
            self.current_window = GalleryWindow(self.evento_path, main_window=self)
            self.current_window.show()

    def close_current_window(self):
        if self.current_window:
            self.current_window.close()
            self.current_window = None
