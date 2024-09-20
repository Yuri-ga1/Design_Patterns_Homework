from general.abstract_files.abstract_model import AbstractReference
from general.settings.models.Settings import Settings
from general.exception.Validator_wrapper import ValidatorWrapper as Validator


class Organization(AbstractReference):
    __inn = ""
    __account = ""
    __bic = ""
    __property_type = ""

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value:str):
        Validator.validate_type(value, str, 'inn')
        Validator.validate_length(value.strip(), 12, 'inn')

        self.__inn = value
        
    
    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value:str):
        Validator.validate_type(value, str, 'account')
        Validator.validate_digits(value.strip(), 11, 'account')

        self.__account = value
        
    
    @property
    def bic(self):
        return self.__bic
    
    @bic.setter
    def bic(self, value:str):
        Validator.validate_type(value, str, 'bic')
        Validator.validate_digits(value.strip(), 9, 'bic')

        self.__bic = value
        
    
    @property
    def property_type(self):
        return self.__property_type
    
    @property_type.setter
    def property_type(self, value:str):
        Validator.validate_type(value, str, 'property_type')
        Validator.validate_length(value.strip(), 9, 'bic')

        self.__property_type = value
        
    def load_settings(self, settings: Settings):
        self.inn = settings.inn
        self.account = settings.account
        self.bic = settings.bic
        self.property_type = settings.property_type
        
    def __eq__(self, other):
        if isinstance(other, Organization):
            return (
                    self.__inn == other.inn and
                    self.__account == other.account and
                    self.__bic == other.bic and
                    self.__property_type == other.property_type
                )
        return NotImplemented
        