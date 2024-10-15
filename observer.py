import os
import logging
import threading
from typing import List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib.pyplot as plt
import matplotlib.animation as animation

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataObserver:
    def __init__(
        self, 
        files: List[str],
    ):
        self.files = files
        self.datas = {
            os.path.basename(file):[]
            for file in self.files
        }
        self.observer = Observer()
        self.lock = threading.Lock()

    def start(self, handler: "FileChangeHandler"):
        for file in self.files:
            self.observer.schedule(
                handler,
                path=os.path.dirname(os.path.abspath(file)) or '.',
                recursive=False
            )

        self.observer.start()

    def join(self):
        self.observer.join()

    def stop(self):
        self.observer.stop()


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, observer: DataObserver):
        self.observer = observer
        self.basenames = [
            os.path.basename(p)
            for p in self.observer.files
        ]

    def on_modified(self, event):
        base_src_path = os.path.basename(event.src_path)
        if base_src_path in self.basenames:
            with open(event.src_path, 'r') as file:
                lines = file.readlines()
                with self.observer.lock:
                    # self.observer.datas[base_src_path].clear()
                    for line in lines:
                        x, y = map(float, line.strip().split(' '))
                        self.observer.datas[base_src_path].append((x, y))
                        print(f"observer: {x}, {y} for {base_src_path}")