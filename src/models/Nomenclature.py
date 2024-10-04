from general.abstract_files.abstract_model import AbstractReference
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
import inspect

class Nomenclature(AbstractReference):
    __name = ""
    __full_name = ""
    __group: NomenclatureGroup = ""
    __unit: MeasurementUnit = ""
    
    def __init__(self, name: str = "", full_name: str = "", group: NomenclatureGroup = None, unit: MeasurementUnit = None):
        if name:
            self.__name = name
        if full_name:
            self.__full_name = full_name
        if group:
            self.__group = group
        if unit:
            self.__unit = unit
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, 'name')
        Validator.validate_max_length(value.strip(), 50, 'name')
        
        self.__name = value
        
        
    @property
    def full_name(self):
        return self.__full_name
    
    @full_name.setter
    def full_name(self, value: str):
        Validator.validate_type(value, str, inspect.currentframe().f_code.co_name)
        Validator.validate_max_length(value.strip(), 255, inspect.currentframe().f_code.co_name)
        
        self.__full_name = value
        
    
    @property
    def group(self):
        return self.__group
    
    @group.setter
    def group(self, value: NomenclatureGroup):
        Validator.validate_type(value, NomenclatureGroup, inspect.currentframe().f_code.co_name)
        
        self.__group = value
    
    
    @property
    def unit(self):
        return self.__unit
    
    @unit.setter
    def unit(self, value: MeasurementUnit):
        Validator.validate_type(value, MeasurementUnit, inspect.currentframe().f_code.co_name)
        
        self.__unit = value
        
    def __eq__(self, other):
        super().__eq__(other)
        