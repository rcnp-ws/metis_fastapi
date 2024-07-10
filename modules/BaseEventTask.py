import threading
import time
from abc import ABC, abstractmethod


class BaseEventTask(ABC, threading.Thread):
    def __init__(self) -> None:
        super(BaseEventTask, self).__init__()
        self._sendBuffer = {}

    @abstractmethod
    def task(self):
        pass

    def run(self):
        self._sendBuffer = self.task()
