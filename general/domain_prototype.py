from general.abstract_files.abstract_prototype import AbstractPrototype
from general.abstract_files.abstract_model import AbstractReference
from general.filter.filter_dto import FilterDTO
from general.filter.filter_matcher import FilterMatcher

from src.emuns.filter_types import FilterTypes

from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.exception.exceptions import ArgumentException, ConversionException

from typing import List

class DomainPrototype(AbstractPrototype):
    __data: List[AbstractReference] = []
    __matcher: FilterMatcher = FilterMatcher()

    def __init__(self, source: List[AbstractReference] = None) -> None:
        super().__init__(source)
        if source:
            self.__data = source

    @property
    def data(self) -> List[AbstractReference]:
        return self.__data

    @data.setter
    def data(self, value: List[AbstractReference]):
        Validator.validate_type(value, list, 'data')
        self.__data = value

    def create(self, data: List[AbstractReference], filt: FilterDTO) -> 'DomainPrototype':
        Validator.validate_type(filt, FilterDTO, 'filt')

        filtered_data = self.filter_by_field(data, filt, 'name')
        filtered_data = self.filter_by_field(filtered_data, filt, 'unique_code')
        
        return DomainPrototype(filtered_data)

    def filter_by_field(self, source: List[AbstractReference], filt: FilterDTO, field: str) -> List[AbstractReference]:
        Validator.validate_not_none(source, 'source')
        Validator.validate_not_none(filt, 'filt')
        Validator.validate_non_empty(field, 'field')

        if not getattr(filt, field, None):
            return source
        
        result = []
        for item in source:
            if self.match_field(getattr(item, field, None), getattr(filt, field), filt.type):
                result.append(item)
            elif self.filter_nested(item, filt, field):
                result.append(item)
        return result

    def filter_nested(self, item: AbstractReference, filt: FilterDTO, field: str) -> bool:
        Validator.validate_not_none(item, 'item')
        Validator.validate_not_none(filt, 'filt')
        Validator.validate_non_empty(field, 'field')

        for attr_name in dir(item):
            attr_value = getattr(item, attr_name)
            if isinstance(attr_value, AbstractReference) and self.match_field(getattr(attr_value, field, None), getattr(filt, field), filt.type):
                return True
            elif isinstance(attr_value, list):
                for nested_item in attr_value:
                    if isinstance(nested_item, AbstractReference) and self.match_field(getattr(nested_item, field, None), getattr(filt, field), filt.type):
                        return True
        return False

    def match_field(self, field_value: str, filter_value: str, filter_type: FilterTypes) -> bool:
        if not field_value or not filter_value:
            return False
        try:
            return self.__matcher.match_field(field_value, filter_value, filter_type)
        except (ArgumentException, ConversionException) as e:
            return False
        except Exception as ex:
            return False
