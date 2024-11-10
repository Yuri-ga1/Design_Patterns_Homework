from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper

class WarehouseModel(AbstractReference):
    __name: str = ""
    __country: str = ""
    __city: str = ""
    __street: str = ""
    __house_number: str = ""
    
    @staticmethod
    def create(
        name: str,
        country: str,
        city: str,
        street: str,
        house_number: str
    ):  
        warehouse = WarehouseModel()
        warehouse.name = name
        warehouse.country = country
        warehouse.city = city
        warehouse.street = street
        warehouse.house_number = house_number
        return warehouse
    

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        ValidatorWrapper.validate_type(value, str, 'warehouse name')
        ValidatorWrapper.validate_max_length(value, 50, "warehouse name")
        self.__name = value.strip()

    @property
    def country(self):
        return self.__country
    
    @country.setter
    def country(self, value: str):
        ValidatorWrapper.validate_type(value, str, 'country')
        self.__country = value.strip()

    @property
    def city(self):
        return self.__city
    
    @city.setter
    def city(self, value: str):
        ValidatorWrapper.validate_type(value, str, 'city')
        self.__city = value.strip()

    @property
    def street(self):
        return self.__street
    
    @street.setter
    def street(self, value: str):
        ValidatorWrapper.validate_type(value, str, 'street')
        self.__street = value.strip()

    @property
    def house_number(self):
        return self.__house_number
    
    @house_number.setter
    def house_number(self, value: str):
        ValidatorWrapper.validate_type(value, str, 'house number')
        self.__house_number = value.strip()

    def __eq__(self, other):
        if isinstance(other, WarehouseModel):
            return (self.__name == other.name and
                    self.__country == other.country and
                    self.__city == other.city and
                    self.__street == other.street and
                    self.__house_number == other.house_number)
        return NotImplemented
