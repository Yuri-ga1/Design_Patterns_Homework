from general.abstract_files.abstract_model import AbstractReference

from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class NomenclatureGroup(AbstractReference):
    __name: str = ""

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, 'name')
        Validator.validate_max_length(value.strip(), 50, 'name')
        self.__name = value.strip()
        
    def __eq__(self, other):
        if isinstance(other, NomenclatureGroup):
            return self.__name == other.name
        return NotImplemented
    
    
    def __hash__(self):
        return hash(self.__name)
    
    """
    Default группа - сырье (фабричный метод)
    """
    @staticmethod
    def default_group_source():
        item = NomenclatureGroup()
        item.name = "Сырье"
        return item
    
    """
    Default группа - заморозка (фабричный метод)
    """
    @staticmethod
    def default_group_cold():
        item = NomenclatureGroup()
        item.name = "Заморозка"
        return item
    