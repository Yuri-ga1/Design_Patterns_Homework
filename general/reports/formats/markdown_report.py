from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class MarkdownReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.MARKDOWN

    def _format_value(self, value, indent_level=0):
        indent = "  " * indent_level
        result = ""

        if hasattr(value, '__dict__'):
            for field in dir(value):
                if not field.startswith("_") and not callable(getattr(value.__class__, field)):
                    field_value = getattr(value, field)
                    result += f"{indent}- {field}: {self._format_value(field_value, indent_level + 1)}"
        elif isinstance(value, (list, tuple)):
            for item in value:
                result += f"{indent}- {self._format_value(item, indent_level + 1)}"
        elif isinstance(value, dict):
            for key, val in value.items():
                result += f"{indent}- {key}: {self._format_value(val, indent_level + 1)}"
        elif value is None:
            result += f"{indent}null\n"
        else:
            result += f"{indent}{str(value)}\n"

        return result

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        for field in fields:
            self.result += f"# {str(field)}\n"
            for row in data:
                value = getattr(row, field)
                self.result += f"{self._format_value(value, 1)}"
            self.result += "\n"
