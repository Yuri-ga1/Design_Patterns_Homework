import json
from datetime import date

from .settings import Settings
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from src.emuns.event_types import EventType

from general.abstract_files.abstract_manager import AbstractManager
from general.abstract_files.abstract_logic import AbstractLogic

class SettingsManager(AbstractManager, AbstractLogic):
    __file_name = "settings.json"
    __settings: Settings = None

    def __init__(self) -> None:
        super().__init__()
        if self.__settings is None:
            self.__settings = self._default_value()
            
    def convert(self, new_dict: dict):
        Validator.validate_type(new_dict, dict, 'new_dict')
        for key, value in new_dict.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    def open(self, file_name: str = ""):
        Validator.validate_type(file_name, str, 'file_name')
        
        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = self._get_file_path(self.__file_name)
            if full_name is None:
                self.__settings = self._default_value()
                Validator.validate_file_exists(self.__file_name)
                
            with open(full_name, 'r', encoding="utf-8") as stream:
                data = json.load(stream)
                self.convert(data)

            return True
        except:
            self.__settings = self._default_value()
            return False

    def save(self):
        if not self.__settings:
            self.__settings = self._default_value()

        settings_dict = {attr: str(getattr(self.__settings, attr)) for attr in dir(self.__settings) if not attr.startswith('_')}

        full_name = self._get_file_path(self.__file_name)

        print(full_name)

        with open(full_name, 'w', encoding='utf-8') as stream:
            json.dump(settings_dict, stream, ensure_ascii=False, indent=4)

    @property
    def settings(self):
        return self.__settings

    def _default_value(self):
        data = Settings()
        data.inn = "012345678901"
        data.organization_name = "Рога и копыта (default)"
        data.account = "01234567890"
        data.correspondent_account = "01234567890"
        data.bic = "012345678"
        data.property_type = "01234"
        data.default_report_format = 'csv'
        data.block_period = date(year=2024, month=10, day=1)

        return data


    def set_exception(self, ex):
        return super().set_exception(ex)
    
    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)
        match type:
            case EventType.CHANGE_BLOCK_PERIOD:
                self.save()