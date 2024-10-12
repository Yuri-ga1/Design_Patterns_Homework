from general.abstract_files.abstract_logic import AbstractLogic


"""
Репозиторий данных
"""
class DataReposity(AbstractLogic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataReposity, cls).__new__(cls)
        return cls.instance 

    """
    Набор данных
    """
    @property
    def data(self):
        return self.__data
    
    @property
    def keys(self):
        return self.__data.keys()
    
    @staticmethod
    def group_key() -> str:
        return "group"
    
    @staticmethod
    def unit_key() -> str:
        return "unit"
    
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"
    
    @staticmethod
    def recipe_key() -> str:
        return "recipes"
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    
    