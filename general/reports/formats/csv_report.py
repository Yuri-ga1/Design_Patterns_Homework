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

        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x )),  dir(first_model) ))

        for field in fields:
            self.result += f"{str(field)};"

        self.result += "\n"    

        for row in data:
            for field in fields:
            
                value = getattr(row, field)
                self.result += f"{str(value)};"
            self.result += "\n"
