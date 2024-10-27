from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper

class WarehouseModel(AbstractReference):
    __name: str = ""
    __country: str = ""
    __city: str = ""
    __street: str = ""
    __house_number: str = ""

    def __init__(
        self,
        name: str = None,
        country: str = None,
        city: str = None,
        street: str = None,
        house_number: str = None
    ):
        if name:
            ValidatorWrapper.validate_type(name, str, "Warehouse name")
            ValidatorWrapper.validate_max_length(name, 50, "Warehouse name")
            self.__name = name.strip()

        if country:
            ValidatorWrapper.validate_type(country, str, "Country")
            self.__country = country.strip()

        if city:
            ValidatorWrapper.validate_type(city, str, "City")
            self.__city = city.strip()

        if street:
            ValidatorWrapper.validate_type(street, str, "Street")
            self.__street = street.strip()

        if house_number:
            ValidatorWrapper.validate_type(house_number, str, "House number")
            self.__house_number = house_number.strip()

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
