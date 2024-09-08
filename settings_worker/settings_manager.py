import json
import os

from .settings import Settings


class SettingsManager:
    """
    Менеджер настроек
    """
    
    __file_name = "settings.json"
    __settings: Settings = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance 
     

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_settings()
            
    
    def convert(self, new_dict: dict):
        if not isinstance(new_dict, dict):
            raise TypeError("Некорректно переданы параметры!")
        for key, value in new_dict.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    
    def open(self, file_name:str = ""):
        """
        Открыть и загрузить настройки
        """
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")
        
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = self.__get_file_path(self.__file_name)
            if full_name is None:
                self.__settings = self.__default_settings()
                raise FileNotFoundError(f"Файл {self.__file_name} не был найден.")
                
            with open (full_name, 'r', encoding="utf-8") as stream:
                data = json.load(stream)
                self.convert(data)

            return True
        except:
            self.__settings = self.__default_settings()
            return False

    
    @property
    def settings(self):
        """
        Загруженные настройки
        """
        return self.__settings
    
    @staticmethod
    def __get_file_path(filename: str):
        curdir = os.curdir
        for address, dirs, files in os.walk(curdir):
            filepath = os.path.join(address, filename)
            if os.path.isfile(filepath):
                return filepath
        return None
    
    
    def __default_settings(self):
        """
        Набор настроек по умолчанию
        """
        data = Settings()
        data.inn = "012345678901"
        data.organization_name = "Рога и копыта (default)"
        data.account = "01234567890"
        data.correspondent_account = "01234567890"
        data.bic = "012345678"
        data.property_type = "01234"

        return data
