from general.exception.exceptions import *
from enum import Enum

class ValidatorWrapper:
    """Класс-обертка для валидации аргументов и выброса соответствующих исключений."""


    @staticmethod
    def validate_not_none(value, field_name: str):
        """Проверяет, что значение не None. Если значение None, выбрасывает исключение."""
        if value is None:
            raise ArgumentException(f"Field '{field_name}' can not be None.")

    @staticmethod
    def validate_length(value: str, length: int, argument_name: str):
        """Проверяет длину строки и выбрасывает LengthException при неккоректной длине."""
        if len(value) != length:
            raise LengthException(argument_name, length)
        
    @staticmethod
    def validate_max_length(value: str, max_length: int, argument_name: str):
        """Проверяет длину строки и выбрасывает LengthException при неккоректной длине."""
        if len(value) > max_length:
            raise MaxLengthException(argument_name, max_length)

    @staticmethod
    def validate_digits(value: str, expected_length: int, argument_name: str):
        """Проверяет, что строка состоит из цифр и имеет нужную длину, иначе выбрасывает DigitsException."""
        if not value.isdigit():
            raise DigitsException(argument_name, expected_length)
        if len(value) != expected_length:
            raise DigitsException(argument_name, expected_length)
        
    @staticmethod
    def validate_positive_integer(value: int, argument_name: str):
        """Проверяет, что значение является положительным целым числом."""
        if not isinstance(value, int):
            raise ArgumentException(argument_name, "Must be an integer")
        if value <= 0:
            raise ValueError(f"'{argument_name}' must be a positive integer")

    @staticmethod
    def validate_type(value, expected_type, argument_name: str):
        """Проверяет тип аргумента и выбрасывает ArgumentException при несоответствии."""
        if not isinstance(value, expected_type):
            raise ArgumentException(argument_name, f"Expected type {expected_type.__name__} but got {type(expected_type)}")

    @staticmethod
    def validate_conversion(value: float, conversion_factor: float):
        """Проверяет корректность коэффициента преобразования и выбрасывает ConversionException."""
        if conversion_factor <= 0:
            raise ConversionException(f"Invalid conversion factor: {conversion_factor}")
        return value * conversion_factor

    @staticmethod
    def validate_file_exists(file_path: str):
        """Проверяет существование файла, иначе выбрасывает NotFoundException."""
        import os
        if not os.path.exists(file_path):
            raise NotFoundException(f"File {file_path}")
        
    @staticmethod
    def validate_non_empty(value: str, argument_name: str):
        """Проверяет, что строка не пустая, иначе выбрасывает ArgumentException."""
        if not value or not value.strip():
            raise ArgumentException(argument_name, "Cannot be empty")
        
    @staticmethod
    def validate_not_empty_dataset(data, argument_name: str = "Dataset"):
        """Проверяет, что набор данных не пустой, иначе выбрасывает EmptyDataSetException."""
        if len(data) == 0:
            raise EmptyDataSetException(f"{argument_name} is empty")
        
    @staticmethod
    def validate_format(format: str, supported_formats: dict):
        """Проверяет, что формат поддерживается, иначе выбрасывает InvalidFormatException."""
        if format not in supported_formats:
            raise InvalidFormatException(format)
    
    @staticmethod
    def validate_module_exists(module_name: str, format_name: str):
        """Проверяет, существует ли модуль, и выбрасывает NotFoundException при его отсутствии."""
        import importlib
        module = importlib.util.find_spec(module_name)
        if module is None:
            raise NotFoundException(f"Module for format {format_name} not found: {module_name}")
        return importlib.import_module(module_name)

    @staticmethod
    def validate_class_exists(module, class_name: str, format_name: str):
        """Проверяет существование класса в модуле и выбрасывает ArgumentException при отсутствии."""
        if not hasattr(module, class_name):
            raise ArgumentException(class_name, f"Class for format {format_name} not found in module {module.__name__}")
        return getattr(module, class_name)
    
    @staticmethod
    def validate_format_in_enum(value: str, enum_class: Enum, argument_name: str):
        """Проверяет, что значение существует в перечислении, игнорируя регистр."""
        ValidatorWrapper.validate_type(value, str, 'validate_format_in_enum "value" must be str')
        if not issubclass(enum_class, Enum):
            raise ArgumentException(argument_name, f"Expected enum class: {enum_class.__name__}")
        if not any(value.upper() == item.name for item in enum_class):
            raise ArgumentException(argument_name, f"Value '{value}' is not a valid format in {enum_class.__name__}")