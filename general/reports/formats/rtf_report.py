from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class RtfReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.RTF
        self.result = ""

    def _format_value(self, value, indent_level=0):
        indent = "\\tab" * indent_level
        result = ""

        if hasattr(value, '__dict__'):
            # Обрабатываем объект
            for field in dir(value):
                if not field.startswith("_") and not callable(getattr(value.__class__, field)):
                    field_value = getattr(value, field)
                    result += f"{indent}\\b {field}: \\b0 " + self._format_value(field_value, indent_level + 1)
        elif isinstance(value, (list, tuple)):
            # Обрабатываем список
            for item in value:
                result += f"{indent}- " + self._format_value(item, indent_level)
        elif isinstance(value, dict):
            # Обрабатываем словарь
            for key, val in value.items():
                result += f"{indent}\\b {key}: \\b0 " + self._format_value(val, indent_level + 1)
        elif value is None:
            result += f"{indent}null\\par\n"
        else:
            result += f"{indent}{str(value)}\\par\n"

        return result

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        self.result += "{\\rtf1\\ansi\\deff0"  # Начало RTF документа

        for row in data:
            self.result += "\\par\n"  # Новый параграф для каждого объекта
            self.result += self._format_value(row)  # Обработка строки
            self.result += "\\par\n"  # Завершение объекта

        self.result += "}"  # Завершение RTF документа
