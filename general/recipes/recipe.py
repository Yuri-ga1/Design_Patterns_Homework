from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class Recipe:
    __name = ""
    __ingredients = {}
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
    def ingredients(self, value: dict):
        Validator.validate_type(value, dict, 'value')
        self.__ingredients = value

    @property
    def steps(self):
        return self.__steps
    
    @steps.setter
    def steps(self, value: list):
        Validator.validate_type(value, list, 'value')
        self.__steps = value
