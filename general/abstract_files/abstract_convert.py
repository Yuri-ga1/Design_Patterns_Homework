import abc
from general.abstract_files.abstract_logic import AbstractLogic
from general.exception.Validator_wrapper import ValidatorWrapper as Validator


class AbstractConvert(AbstractLogic):
    
    """
    Сконвертировать объект в словарь
    """
    @abc.abstractmethod
    def serialize(self, field: str, object) -> dict:
        Validator.validate_type(field, str, 'field')
        self.__error_text = ""

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)     