from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class MarkdownReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.MARKDOWN

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        # Заголовки и пункты
        for field in fields:
            self.result += f"# {str(field)}\n"  # Заголовок

            # Данные под заголовком
            for row in data:
                value = getattr(row, field)
                if hasattr(value, 'name'):
                    value = value.name  # Используем имя объекта
                
                # Обработка списка или словаря
                if isinstance(value, (list, dict)):
                    for item in value:
                        self.result += f"- {str(item)}\n"  # Каждый элемент на новой строке
                elif isinstance(value, str) and '\n' in value:
                    value_lines = value.split('\n')
                    self.result += f"- {'<br>'.join(value_lines)}\n"  # Добавляем многострочные строки
                else:
                    self.result += f"- {str(value)}\n"  # Пункт

            self.result += "\n"  # Пустая строка между заголовками
