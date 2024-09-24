from general.abstract_files.abstract_logic import AbstractLogic
from general.abstract_files.abstract_report import AbstractReport
from src.emuns.format_reporting import FormatReporting
from general.reports.csv_report import CsvReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
# operation_exception


"""
Фабрика для формирования отчетов
"""
class ReportFactory(AbstractLogic):
    __reports = {}

    def __init__(self) -> None:
        super().__init__()
        # Наборы отчетов
        self.__reports[ FormatReporting.CSV ] = CsvReport


    """
    Получить инстанс нужного отчета
    """
    def create(self, format: FormatReporting) ->  AbstractReport: 
        Validator.validate_type(format, FormatReporting, 'format')
        Validator.validate_format(format, self.__reports.keys())
        
        report = self.__reports[format]
        return report()
    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
       



    
