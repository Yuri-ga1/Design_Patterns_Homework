from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class RtfReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.RTF

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        # Заголовок
        self.result += "{\\rtf1\\ansi\\deff0"
        for field in fields:
            self.result += f"\\b {str(field)} \\b0\t"

        self.result += "\\par\n"

        # Данные
        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"{str(value)}\t"
            self.result += "\\par\n"
        
        self.result += "}"
