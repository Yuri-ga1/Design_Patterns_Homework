from abc import ABC, abstractmethod
from general.exception.Validator_wrapper import ValidatorWrapper
from src.emuns.event_types import EventType

class AbstractLogic(ABC):
    __error_text: str = ""
    
    @property
    def error_text(self) -> str:
        return self.__error_text.strip()
    
    @error_text.setter
    def error_text(self, message: str):
        self.__error_text = message.strip()
    
    
    @property
    def is_error(self) -> bool:
        return False if self.error_text == "" else True
    
    
    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"
    
    
    """
    Абстрактный метод
    """
    @abstractmethod
    def set_exception(self, ex: Exception):
        pass
    
    
    @abstractmethod
    def handle_event(self, type: EventType, params):
        from main import logger
        ValidatorWrapper.validate_type(type, EventType, "type")
        logger.info(f"Handle event with type {type} and params {params}")
     