from general.exception.exceptions import *


class ValidatorWrapper:
    """Класс-обертка для валидации аргументов и выброса соответствующих исключений."""

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
            raise ArgumentException(argument_name, f"Expected type {expected_type.__name__}")

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