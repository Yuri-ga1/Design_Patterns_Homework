from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.emuns.format_reporting import FormatReporting
from src.emuns.logging_levels import LogLevel

from datetime import date

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
    __block_period: date = ""
    __is_first_start: bool = True
    __data_source: str = ""
    __file_log_level: LogLevel = LogLevel.INFO
    __console_log_level: LogLevel = LogLevel.DEBUG
    __enable_console: bool = True
    __log_filename =  ""

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
        
    @property
    def block_period(self):
        return self.__block_period
    
    @block_period.setter
    def block_period(self, value: date):
        Validator.validate_type(value, date, 'block_period value')
        
        self.__block_period = value
        
    @property
    def is_first_start(self):
        return self.__is_first_start
    
    @is_first_start.setter
    def is_first_start(self, value: bool):
        Validator.validate_type(value, bool, 'is_first_start value')
        
        self.__is_first_start = value
        
    
    @property
    def data_source(self):
        return self.__data_source
    
    @data_source.setter
    def data_source(self, value: str | None):
        if value is not None:
            Validator.validate_type(value, str, 'data_source value')
        
        self.__data_source = value
        
    @property
    def file_log_level(self):
        return self.__file_log_level
    
    @file_log_level.setter
    def file_log_level(self, value: LogLevel | None):
        if value is not None:
            Validator.validate_type(value, LogLevel, 'file_log_level value')
        
        self.__file_log_level = value
        
    
    @property
    def console_log_level(self):
        return self.__console_log_level
    
    @console_log_level.setter
    def console_log_level(self, value: LogLevel | None):
        if value is not None:
            Validator.validate_type(value, LogLevel, 'console_log_level value')
        
        self.__console_log_level = value
        
        
    @property
    def enable_console(self):
        return self.__enable_console
    
    @enable_console.setter
    def enable_console(self, value: bool | None):
        if value is not None:
            Validator.validate_type(value, bool, 'enable_console value')
        
        self.__enable_console = value
        
    @property
    def log_filename(self):
        return self.__log_filename
    
    @log_filename.setter
    def log_filename(self, value: str | None):
        if value is not None:
            Validator.validate_type(value, str, 'log_filename value')
        
        self.__log_filename = value
        
    