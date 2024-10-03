import json
from general.exception.Validator_wrapper import ValidatorWrapper
from general.abstract_files.abstract_deserializer import AbstractDeserializer

class JsonDeserializer(AbstractDeserializer):
    def deserialize(self, file_path: str):
        """
        Десериализует содержимое JSON-файла в объекты классов.
        """
        ValidatorWrapper.validate_file_exists(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        ValidatorWrapper.validate_type(data, list, "data")
        ValidatorWrapper.validate_not_empty_dataset(data, "data")

        objects = []
        for item in data:
            ValidatorWrapper.validate_type(item, dict, "item")
            objects.append(self._dict_to_object(item))
        
        return objects
