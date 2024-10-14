from src.emuns.filter_types import FilterTypes
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.abstract_files.abstract_logic import AbstractLogic
from general.exception.exceptions import ArgumentException

class FilterDTO(AbstractLogic):
    __name: str = ""
    __unique_code: str = ""
    __type: FilterTypes = FilterTypes.EQUALS
    
    def __init__(self, name: str = "", unique_code: str = "", type_value: FilterTypes = FilterTypes.EQUALS):
        if name:
            self.name = name
        if unique_code:
            self.unique_code = unique_code
        if type_value:
            self.type = type_value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, 'name')
        Validator.validate_max_length(value.strip(), 50, 'name')
        self.__name = value.strip()

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    @unique_code.setter
    def unique_code(self, value: str):
        Validator.validate_type(value, str, 'unique_code')
        self.__unique_code = value

    @property
    def type(self) -> FilterTypes:
        return self.__type

    @type.setter
    def type(self, value: FilterTypes):
        Validator.validate_format_in_enum(value.value, FilterTypes, 'type')
        self.__type = value

    @staticmethod
    def from_json(data: dict):
        Validator.validate_type(data, dict, "data")
        try:
            name = data.get('name', "")
            unique_code = data.get('unique_code', "")
            type_value = data.get('type', FilterTypes.EQUALS.value)

            Validator.validate_max_length(name, 50, 'name')
            Validator.validate_max_length(unique_code, 20, 'unique_code')
            Validator.validate_format_in_enum(type_value, FilterTypes, 'type')
            type_value = FilterTypes(type_value)
            
            return FilterDTO(
                name=name,
                unique_code=unique_code,
                type_value=type_value
            )
        except ArgumentException as ex:
            FilterDTO().set_exception(ex)
        except Exception as ex:
            FilterDTO().set_exception(ex)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def __eq__(self, other):
        if isinstance(other, FilterDTO):
            return (self.__name == other.name and
                    self.__unique_code == other.unique_code and
                    self.__type == other.type)
        return NotImplemented
