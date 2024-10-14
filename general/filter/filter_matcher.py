from src.emuns.filter_types import FilterTypes
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class FilterMatcher:
    def __init__(self):
        self.matching_functions = {ft: getattr(self, ft.name.lower()) for ft in FilterTypes}

    def match_field(self, field_value: str, filter_value: str, filter_type: FilterTypes) -> bool:
        if filter_type in self.matching_functions:
            return self.matching_functions[filter_type](field_value, filter_value)
        return False

    def equals(self, field_value: str, filter_value: str) -> bool:
        Validator.validate_non_empty(field_value, "field_value")
        Validator.validate_non_empty(filter_value, "filter_value")
        return field_value == filter_value

    def like(self, field_value: str, filter_value: str) -> bool:
        Validator.validate_non_empty(field_value, "field_value")
        Validator.validate_non_empty(filter_value, "filter_value")
        return filter_value in field_value
