from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class MeasurementUnit(AbstractReference):
    __name = ""
    __unit: 'MeasurementUnit' = None
    __conversion_rate = 1

    def __init__(self, name: str = "", unit: 'MeasurementUnit' = None, conversion_rate: int = 1):
        if name:
            Validator.validate_type(name, str, "name")
            self.name = name
        if unit:
            self.set_base_unit(unit, conversion_rate)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, 'name')
        Validator.validate_max_length(value.strip(), 50, 'name')
        
        self.__name = value.strip()

    @property
    def unit(self):
        return self.__unit

    @property
    def conversion_rate(self) -> int:
        return self.__conversion_rate
    
    def set_base_unit(self, unit: 'MeasurementUnit', conversion_rate: int):
        Validator.validate_type(unit, MeasurementUnit, 'unit')
        Validator.validate_type(conversion_rate, int, 'conversion_rate')
        Validator.validate_positive_integer(conversion_rate, 'conversion_rate')
        
        self.__unit = unit
        self.__conversion_rate = conversion_rate
        
    def __eq__(self, other):
        if isinstance(other, MeasurementUnit):
            return (self.__name == other.name and
                    self.__unit == other.unit and
                    self.__conversion_rate == other.conversion_rate)
        return NotImplemented
