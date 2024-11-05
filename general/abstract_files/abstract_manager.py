import os
from abc import ABC, abstractmethod

class AbstractManager(ABC):
    _instance = None
    __banned_dirs = ['.vscode']

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
        banned_dirs = AbstractManager.__banned_dirs
        
        for address, dirs, files in os.walk(curdir):
            if any(banned_dir in address for banned_dir in banned_dirs):
                continue
        
            filepath = os.path.join(address, filename)
            if os.path.isfile(filepath):
                return filepath
        return None

    @abstractmethod
    def _default_value(self):
        pass
