import json

from general.abstract_files.abstract_manager import AbstractManager
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.data_reposity.data_reposity import DataReposity
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager

from general.start_service import StartService

class DataReposityManager(AbstractManager):
    __reposity: DataReposity = None
    __service: StartService = None

    def __init__(self, reposity: DataReposity, settings_manager: SettingsManager, recipe_manager: RecipeManager) -> None:
        super().__init__()
        Validator.validate_type(reposity, DataReposity, 'reposity')
        Validator.validate_type(settings_manager, SettingsManager, 'settings_manager')
        Validator.validate_type(recipe_manager, RecipeManager, 'recipe_manager')
        self.__reposity = reposity
        self.__service = StartService(
            reposity=self.__reposity,
            settings_manager=settings_manager,
            recipe_manager=recipe_manager,
        )
        
    
    def open(self, file_name: str):
        Validator.validate_type(file_name, str, 'file_name')

        try:
            full_name = self._get_file_path(file_name)
            Validator.validate_file_exists(full_name)
                
            with open(full_name, 'r', encoding="utf-8") as stream:
                data = json.load(stream)
                # self.convert(data)
                self.__reposity.data = data

            return True
        except Exception:
            self._default_value()
            return False
    
    def _default_value(self):
        self.__service.create()
        
    @property
    def reposity(self):
        return self.__reposity
    