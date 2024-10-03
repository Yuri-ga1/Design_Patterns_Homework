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
            result_dict = self._object_to_dict(row)
            result_list.append(result_dict)
        
        self.result = json.dumps(result_list, ensure_ascii=False, indent=4)

    def _object_to_dict(self, obj):
        """
        Преобразуем объект в словарь. Если поле объекта также является объектом,
        рекурсивно вызываем преобразование.
        Добавляем название класса объекта.
        """
        result = {
            "__class__": obj.__class__.__name__  # Добавляем имя класса
        }
        for field in dir(obj):
            if not field.startswith("_") and not callable(getattr(obj.__class__, field)):
                value = getattr(obj, field)

                if hasattr(value, "__dict__"):
                    result[field] = self._object_to_dict(value)
                elif isinstance(value, (list, tuple)):
                    result[field] = [self._object_to_dict(item) if hasattr(item, "__dict__") else item for item in value]
                elif hasattr(value, 'name'):
                    result[field] = value.name
                else:
                    result[field] = value
                    
        return result
