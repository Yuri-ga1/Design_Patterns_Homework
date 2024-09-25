from abc import ABC, abstractmethod
from src.emuns.format_reporting import FormatReporting
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
import os
from datetime import datetime as dt


class AbstractReport(ABC):
    __format: FormatReporting = FormatReporting.CSV
    __result:str = ""


    def save_report(self, path: str, report_name: str = None, format: FormatReporting = FormatReporting.CSV):
        Validator.validate_type(path, str, 'path')
        Validator.validate_format_in_enum(format.value, FormatReporting, 'format')

        folder_path = os.path.join(path, format.value)
        os.makedirs(folder_path, exist_ok=True)

        if not report_name:
            report_name = f"report_{dt.now().strftime('%Y%m%d_%H%M%S')}.{format.value}"

        report_file_path = os.path.join(folder_path, report_name)

        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(self.result)
        

    @abstractmethod
    def create(self, data: list):
        pass

    @property
    def format(self) -> FormatReporting:
        return self.__format
    
    @property
    def result(self) -> str:
        return self.__result
    
    @result.setter
    def result(self, value:str):
        Validator.validate_type(value, str, 'value')
        self.__result = value