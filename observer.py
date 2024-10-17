import os
import logging
import threading
from typing import List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from filelock import FileLock

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
        self.file_locks = {
            os.path.basename(file): f"{file}.lock"
            for file in self.files
        }
        self.line_offsets = {
            os.path.basename(file): 0
            for file in self.files
        }

    def start(self, handler: "FileChangeHandler"):
        print("DataObServer start")
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
            with FileLock(self.observer.file_locks[base_src_path]):
                with open(event.src_path, 'r') as file:
                    cur_line_offset = 0
                    for line in file:
                        if self.observer.line_offsets[base_src_path] > cur_line_offset:
                            cur_line_offset += 1
                            continue
                        with self.observer.lock:
                            x, y = map(float, line.strip().split(' '))
                            self.observer.datas[base_src_path].append((x, y))
                            print(f"observer: {base_src_path}: {self.observer.datas[base_src_path]}")
                        cur_line_offset += 1
                    self.observer.line_offsets[base_src_path] = cur_line_offset
