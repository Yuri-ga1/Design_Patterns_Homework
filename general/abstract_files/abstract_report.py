from abc import ABC, abstractmethod
from src.emuns.format_reporting import FormatReporting
from general.exception.Validator_wrapper import ValidatorWrapper as Validator



class AbstractReport(ABC):
    __format: FormatReporting = FormatReporting.CSV
    __result:str = ""


    @abstractmethod
    def create(self, data: list):
        pass

    @property
    def format(self) -> FormatReporting:
        return self.__format
    
    @property
    def result(self) -> str:
        return self.__result
    
    @result.setter
    def result(self, value:str):
        Validator.validate_type(value, str, 'value')
        self.__result = value