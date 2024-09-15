class BaseException(Exception):
    """Базовый класс для всех ошибок."""
    pass

class ArgumentException(BaseException):
    """Исключение для ошибок, связанных с аргументами."""
    def __init__(self, argument_name: str, message: str = "Invalid argument"):
        self.argument_name = argument_name
        self.message = f"{message}: {argument_name}"
        super().__init__(self.message)

class LengthException(ArgumentException):
    """Исключение для ошибок, связанных с длиной строки."""
    def __init__(self, argument_name: str, length: int):
        self.message = f"Length of '{argument_name}' exceeds the allowed limit of {length} characters"
        super().__init__(argument_name, self.message)
        
class MaxLengthException(ArgumentException):
    """Исключение для ошибок, связанных с максимальной длиной строки."""
    def __init__(self, argument_name: str, max_length: int):
        self.message = f"Length of '{argument_name}' exceeds the allowed limit of {max_length} characters"
        super().__init__(argument_name, self.message)

class DigitsException(ArgumentException):
    """Исключение для ошибок, связанных с длиной строки и цифрами."""
    def __init__(self, argument_name: str, length: int):
        self.message = f"'{argument_name}' must contain {length} digits"
        super().__init__(argument_name, self.message)

class ConversionException(BaseException):
    """Исключение для ошибок преобразования единиц измерения."""
    def __init__(self, message: str = "Invalid conversion"):
        super().__init__(message)

class NotFoundException(BaseException):
    """Исключение для ошибок, связанных с отсутствием файла или данных."""
    def __init__(self, item: str = "File or item"):
        super().__init__(f"{item} not found")
        