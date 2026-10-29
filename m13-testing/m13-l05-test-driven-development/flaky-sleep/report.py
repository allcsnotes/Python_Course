import random
import threading
import time


class Report:
    def __init__(self):
        self.ready = False

    def _build(self):
        time.sleep(random.uniform(0.01, 0.1))
        self.ready = True

    def start(self):
        worker = threading.Thread(target=self._build)
        worker.start()
        return worker
