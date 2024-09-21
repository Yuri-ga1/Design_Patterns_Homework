import os
from abc import ABC, abstractmethod

class AbstractManager(ABC):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AbstractManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._default_value()
            self._initialized = True

    @abstractmethod
    def open(self, file_name: str = ""):
        pass

    @staticmethod
    def _get_file_path(filename: str):
        curdir = os.curdir
        for address, dirs, files in os.walk(curdir):
            filepath = os.path.join(address, filename)
            if os.path.isfile(filepath):
                return filepath
        return None

    @abstractmethod
    def _default_value(self):
        pass
