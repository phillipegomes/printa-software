
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if event.src_path.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
            time.sleep(1)
            self.callback(event.src_path)

class FileWatcher:
    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.observer = Observer()

    def start(self):
        event_handler = ImageHandler(self.callback)
        self.observer.schedule(event_handler, self.path, recursive=False)
        self.observer.start()
