from general.abstract_files.abstract_convert import AbstractConvert
from general.abstract_files.abstract_model import AbstractReference
from general.abstract_files.abstract_logic import AbstractLogic
from general.base_models import BaseModelCode, BaseModelName
from general.common import Common
from general.exception.Validator_wrapper import ValidatorWrapper
from general.exception.exceptions import OperationException
import datetime


class BasicConvertor(AbstractConvert):
    
    def serialize(self, field: str, object) -> dict:
        super().serialize(field, object)

        ValidatorWrapper.validate_type(object, (int, str, bool, float), "object")  # Validate object type

        try:
            return {field: object}
        except Exception as ex:
            self.set_exception(ex)

        return None


class DatetimeConvertor(AbstractConvert):
    
    def serialize(self, field: str, object):
        super().serialize(field, object)

        ValidatorWrapper.validate_type(object, datetime.datetime, "object")  # Validate object type

        try:
            return {field: object.strftime('%Y-%m-%d')}
        except Exception as ex:
            self.set_exception(ex)    

        return None  # Added return statement to ensure a consistent return type


class ReferenceConvertor(AbstractConvert):
    
    def serialize(self, field: str, object: AbstractReference) -> dict:
        super().serialize(field, object)

        factory = ConvertFactory()
        return factory.serialize(object)


class ConvertFactory(AbstractLogic):
    _maps = {}
    
    def __init__(self) -> None:
        # Связка с простыми типами
        self._maps[datetime.datetime] = DatetimeConvertor
        self._maps[int] = BasicConvertor
        self._maps[float] = BasicConvertor
        self._maps[str] = BasicConvertor
        self._maps[bool] = BasicConvertor
        
        # Связка для всех моделей
        for inheritor in BaseModelName.__subclasses__():
            self._maps[inheritor] = ReferenceConvertor    

        for inheritor in BaseModelCode.__subclasses__():
            self._maps[inheritor] = ReferenceConvertor        
    
    def serialize(self, object) -> dict:
        result = self.__convert_list("data", object)
        if result is not None:
            return result
        
        result = {}
        fields = Common.get_fields(object)
        
        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)
                
                dictionary = self.__convert_list(field, value)
                if dictionary is None:
                    dictionary = self.__convert_item(field, value)
                    
                if len(dictionary) == 1:
                    result[field] = dictionary[field]
                else:
                    result[field] = dictionary       
          
        return result  
    
    def __convert_item(self, field: str, source):
        ValidatorWrapper.validate_type(field, str, 'field')
        if source is None:
            return {field: None}
        
        if type(source) not in self._maps.keys():
            raise OperationException(f"Не возможно подобрать конвертор для типа {type(source)}")

        convertor = self._maps[type(source)]()
        dictionary = convertor.serialize(field, source)
        
        if convertor.is_error:
            raise OperationException(f"Ошибка при конвертации данных {convertor.error_text}")
        
        return dictionary
            
    def __convert_list(self, field: str, source) -> list:
        ValidatorWrapper.validate_type(field, str, 'field')
        
        if isinstance(source, list):
            result = []
            for item in source:
                if isinstance(item, (str, int, float, bool)):
                    result.append(item)
                else:    
                    result.append(self.__convert_item(field, item))  
            
            return result 
        
        if isinstance(source, dict):
            result = {}
            for key, object in source.items():
                value = self.__convert_item(key, object)
                result[key] = value
                
            return result 
        
        return None 

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
