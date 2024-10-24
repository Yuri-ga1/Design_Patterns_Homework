from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class MeasurementUnit(AbstractReference):
    __name = ""
    __unit: 'MeasurementUnit' = None
    __conversion_rate: 'MeasurementUnit | int' = 1

    def __init__(self, name: str = "", unit: 'MeasurementUnit' = None, conversion_rate: 'MeasurementUnit | int' = 1):
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
    
    @unit.setter
    def unit(self, value: 'MeasurementUnit'):
        if value:
            Validator.validate_type(value, MeasurementUnit, 'unit')
        
        self.__unit = value

    @property
    def conversion_rate(self) -> 'MeasurementUnit | int':
        return self.__conversion_rate
    
    @conversion_rate.setter
    def conversion_rate(self, value: 'MeasurementUnit | int'):
        if value:
            if isinstance(value, MeasurementUnit):
                Validator.validate_type(value, MeasurementUnit, 'conversion_rate')
            elif isinstance(value, int):
                Validator.validate_positive_integer(value, 'conversion_rate')
            else:
                raise TypeError("conversion_rate должен быть либо целым числом, либо объектом MeasurementUnit")
        
        self.__conversion_rate = value
    
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
    
    
    def __hash__(self):
        return hash((self.__name, self.__unit, self.__conversion_rate))
    
    @staticmethod
    def default_unit_gramm():
        gramm = MeasurementUnit("Грамм")
        return gramm
    
    @staticmethod
    def default_unit_kg():
        gramm = MeasurementUnit.default_unit_gramm()
        kg = MeasurementUnit("Килограмм", gramm, 1000)
        return kg
    
    @staticmethod
    def default_unit_thing():
        thing = MeasurementUnit("Штука")
        return thing
    
    @staticmethod
    def default_unit_teaspoon():
        teaspoon = MeasurementUnit("Чайная ложка")
        return teaspoon
    
    @staticmethod
    def default_unit_tablespoon():
        teaspoon = MeasurementUnit.default_unit_teaspoon()
        tablespoon = MeasurementUnit("Столовая ложка", teaspoon, 3)
        return tablespoon
