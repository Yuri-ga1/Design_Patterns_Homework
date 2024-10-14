from abc import ABC, abstractmethod
from general.exception.Validator_wrapper import ValidatorWrapper


class AbstractPrototype(ABC):
    __data = []
    
    
    def __init__(self, data: list) -> None:
        super().__init__()
        self.__data = data
    
    @property
    def data(self):
        return self.__data    
    
    @data.setter
    def data(self, value: list):
        ValidatorWrapper.validate_type(value, list, 'value')
        self.__data = value
        
    @abstractmethod
    def create(self, data: list, filter):
        pass