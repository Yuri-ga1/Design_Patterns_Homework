from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
import json

class JsonReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.JSON

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        # Преобразуем список объектов в список словарей
        result_list = []
        for row in data:
            result_dict = {}
            for field in dir(row):
                if not field.startswith("_") and not callable(getattr(row.__class__, field)):
                    value = getattr(row, field)
                    if hasattr(value, 'name'):
                        value = value.name  # Используем имя объекта
                    result_dict[field] = value
            result_list.append(result_dict)
        
        self.result = json.dumps(result_list, ensure_ascii=False, indent=4)

