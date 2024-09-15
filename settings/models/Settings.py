
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

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 12 or not value.isdigit():
            raise ValueError("Длинна ИНН обязанна быть 12 цифр!")

        self.__inn = value
        
    
    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11 or not value.isdigit():
            raise ValueError("Длинна счета обязанна быть 11 цифр!")

        self.__account = value
        
    
    @property
    def correspondent_account(self):
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 11 or not value.isdigit():
            raise ValueError("Длинна корреспондентского счета обязанна быть 11 цифр!")

        self.__correspondent_account = value
        
    
    @property
    def bic(self):
        return self.__bic
    
    @bic.setter
    def bic(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 9 or not value.isdigit():
            raise ValueError("Длинна БИК обязанна быть 9 цифр!")

        self.__bic = value
        
    
    @property
    def property_type(self):
        return self.__property_type
    
    @property_type.setter
    def property_type(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Некорректно переданы параметры!")
        if len(value) != 5:
            raise ValueError("Вид собственности обязанн содержать 5 символов!")

        self.__property_type = value