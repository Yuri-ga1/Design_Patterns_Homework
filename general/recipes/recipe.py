from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from typing import List
from src.models.Nomenclature import Nomenclature

class Recipe:
    __name = ""
    __ingredients: List[Nomenclature] = []
    __steps = []

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        Validator.validate_type(value, str, 'value')
        self.__name = value

    @property
    def ingredients(self):
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value: List[Nomenclature]):
        Validator.validate_type(value, list, 'value')
        for item in value:
            Validator.validate_type(item, Nomenclature, 'ingredient')
        self.__ingredients = value

    @property
    def steps(self):
        return self.__steps
    
    @steps.setter
    def steps(self, value: list):
        Validator.validate_type(value, list, 'value')
        self.__steps = value
