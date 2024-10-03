import os
import importlib
import inspect
from typing import Dict
from abc import ABC, abstractmethod
from general.exception.Validator_wrapper import ValidatorWrapper

class AbstractDeserializer(ABC):
    __class_mapping: dict = {}
    __models_path: str = 'src/models'
    
    def __init__(self):
        self._generate_class_mapping()
    
    @property
    def class_mapping(self) -> dict:
        return self.__class_mapping
    
    @class_mapping.setter
    def class_mapping(self, value: dict):
        self.__class_mapping = value

    def _generate_class_mapping(self):
        """
        Проходит по всем модулям в директории моделей и собирает все классы.
        """
        for root, _, files in os.walk(self.__models_path):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = os.path.splitext(file)[0]
                    full_module_path = f"{self.__models_path.replace('/', '.')}.{module_name}"
                    try:
                        module = importlib.import_module(full_module_path)
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if obj.__module__ == full_module_path:
                                self.__class_mapping[name] = obj
                    except Exception as e:
                        print(f"Ошибка импорта модуля {full_module_path}: {e}")

    @abstractmethod
    def deserialize(self, data: str):
        pass

    def _dict_to_object(self, data: dict):
        """
        Преобразует словарь обратно в объект класса, используя маппинг.
        """
        ValidatorWrapper.validate_type(data, dict, "data")
        
        class_name = data.pop("__class__", None)
        if not class_name:
            raise ValueError("Поле __class__ отсутствует или пустое")
        
        target_class = self.__class_mapping.get(class_name)
        if not target_class:
            raise ValueError(f"Класс {class_name} не найден в маппинге классов")

        obj = target_class.__new__(target_class)
        
        for field, value in data.items():
            if isinstance(value, dict) and "__class__" in value:
                nested_obj = self._dict_to_object(value)
                setattr(obj, field, nested_obj)
            elif isinstance(value, list):
                list_of_objects = []
                for item in value:
                    if isinstance(item, dict) and "__class__" in item:
                        list_of_objects.append(self._dict_to_object(item))
                    else:
                        list_of_objects.append(item)
                setattr(obj, field, list_of_objects)
            else:
                setattr(obj, field, value)

        return obj
