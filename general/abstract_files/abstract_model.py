import uuid

from abc import ABC, abstractmethod

class AbstractReference(ABC):
    __id: str = str(uuid.uuid4())
    __name: str = ""
    
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
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        if not value.strip():
            raise ValueError("Значение 'name' не может быть пустым!")
        if len(value) > 50:
            raise ValueError("Значение 'name' не может быть длинее 50 символов!")
        self.__name = value

    
    @abstractmethod
    def __eq__(self, other):
        if isinstance(other, AbstractReference):
            return self.__id == other.id
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)

    