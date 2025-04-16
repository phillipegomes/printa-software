import os
from PyQt6.QtCore import QFileSystemWatcher, QObject, pyqtSignal

class FileWatcher(QObject):
    pasta_alterada = pyqtSignal(str)

    def __init__(self, pasta):
        super().__init__()
        self.pasta = pasta
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(pasta)
        self.watcher.directoryChanged.connect(self.on_directory_changed)

    def on_directory_changed(self, path):
        print(f"[🔄 FileWatcher] Alteração detectada em: {path}")
        self.pasta_alterada.emit(path)
