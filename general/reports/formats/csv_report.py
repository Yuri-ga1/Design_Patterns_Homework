from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator


class CsvReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.CSV

    def _format_value(self, value):
        """Форматирует значение для CSV, обрабатывая вложенные структуры."""
        if hasattr(value, '__dict__'):
            return {field: self._format_value(getattr(value, field)) for field in dir(value) if not field.startswith("_") and not callable(getattr(value.__class__, field))}
        elif isinstance(value, (list, tuple)):
            return ', '.join(map(str, value))
        elif isinstance(value, dict):
            return ', '.join([f"{k}:{v}" for k, v in value.items()])
        else:
            return str(value)

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        first_model = data[0]

        # Определяем поля для выгрузки
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        # Добавляем заголовки полей
        headers = []
        for field in fields:
            headers.append(field)
        self.result += ';'.join(headers) + "\n"

        for row in data:
            row_values = []
            for field in fields:
                value = getattr(row, field)
                formatted_value = self._format_value(value)
                
                # Преобразуем вложенные словари в строку
                if isinstance(formatted_value, dict):
                    formatted_value = ', '.join([f"{k}: {v}" for k, v in formatted_value.items()])
                    
                row_values.append(str(formatted_value))
            self.result += ';'.join(row_values) + "\n"