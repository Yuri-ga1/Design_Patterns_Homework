from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.emuns.format_reporting import FormatReporting

class Settings:
    """
    Настройки
    """
    __organization_name = ""
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bic = ""
    __property_type = ""
    __default_report_format = ""

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value:str):
        Validator.validate_type(value, str, 'value')
        
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value:str):
        Validator.validate_type(value, str, 'value')
        Validator.validate_digits(value, 12, 'value')

        self.__inn = value
        
    
    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value:str):
        Validator.validate_type(value, str, 'value')
        Validator.validate_digits(value, 11, 'value')

        self.__account = value
        
    
    @property
    def correspondent_account(self):
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value:str):
        Validator.validate_type(value, str, 'value')
        Validator.validate_digits(value, 11, 'value')

        self.__correspondent_account = value
        
    
    @property
    def bic(self):
        return self.__bic
    
    @bic.setter
    def bic(self, value:str):
        Validator.validate_type(value, str, 'value')
        Validator.validate_digits(value, 9, 'value')

        self.__bic = value
        
    
    @property
    def property_type(self):
        return self.__property_type
    
    @property_type.setter
    def property_type(self, value:str):
        Validator.validate_type(value, str, 'value')
        Validator.validate_length(value, 5, 'value')
        
        self.__property_type = value
        
    @property
    def default_report_format(self):
        return self.__default_report_format
    
    @default_report_format.setter
    def default_report_format(self, value:str):
        Validator.validate_type(value, str, 'value')
        
        self.__default_report_format = value