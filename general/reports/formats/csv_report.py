from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator


class CsvReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.CSV

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        first_model = data[0]

        # Определяем поля для выгрузки
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        # Добавляем заголовки полей
        for field in fields:
            self.result += f"{str(field)};"

        self.result += "\n"

        for row in data:
            for field in fields:
                value = getattr(row, field)

                if hasattr(value, 'name'):
                    value = value.name
                elif isinstance(value, dict):
                    value = ', '.join([f"{k}:{v}" for k, v in value.items()])
                elif isinstance(value, (list, tuple, set)):
                    value = ', '.join(map(str, value))
                else:
                    value = str(value)

                self.result += f"{value};"

            self.result += "\n"
