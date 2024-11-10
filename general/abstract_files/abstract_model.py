import uuid

from abc import ABC, abstractmethod

from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class AbstractReference(ABC):
    def __init__(self):
        self.__id: str = uuid.uuid4().hex
        self.__name: str = ""
    
    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, new_id: str):
        self.__id = new_id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str): 
        Validator.validate_type(value, str, 'name')
        Validator.validate_max_length(value, 50, 'value')
        self.__name = value

    
    @abstractmethod
    def __eq__(self, other):
        if isinstance(other, AbstractReference):
            return self.__id == other.id
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)

    