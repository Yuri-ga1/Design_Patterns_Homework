from general.abstract_files.abstract_model import AbstractReference
from typing import Dict
from abc import ABC, abstractmethod
from general.exception.Validator_wrapper import ValidatorWrapper
from datetime import datetime

from src.emuns.transaction_types import TransactionTypes

class AbstractDeserializer(ABC):
    __class_mapping: dict = {}
    
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
        Проходит по всем наследникам AbstractReference и формирует словарь.
        """
        for subclass in AbstractReference.__subclasses__():
            self.__class_mapping[subclass.__name__] = subclass

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
            
            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
                try:
                    value = TransactionTypes[value]
                except KeyError:
                    pass
                setattr(obj, field, value)
                
            elif isinstance(value, dict) and "__class__" in value:
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
