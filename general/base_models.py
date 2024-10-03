from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper

"""
Базовый класс для наследования с поддержкой сравнения по коду
"""
class BaseModelCode(AbstractReference):

    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other):
        return super().__eq__(other)

"""
Базовый класс для наследования с поддержкой сравнения по наименованию
"""    
class BaseModelName(AbstractReference):
    __name:str = ""

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self.__name.strip()

    @name.setter
    def name(self, value:str):
        ValidatorWrapper.validate_type(value, str, 'value')
        ValidatorWrapper.validate_max_length(value, 255, 'value')
        self.__name = value

    def __eq__(self, other:'BaseModelName'):
        if other is  None: return False
        if not isinstance(other, BaseModelName): return False

        return self.name ==  other.name
