import os

from general.abstract_files.abstract_logic import AbstractLogic
from general.data_reposity import DataReposity
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from general.settings.settings_manager import SettingsManager
from general.settings.settings import Settings
from general.recipes.recipe_manager import RecipeManager

from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomeclature_group import NomenclatureGroup


"""
Сервис для реализации первого старта приложения
"""
class StartService(AbstractLogic):
    __reposity: DataReposity = None
    __settings_manager: SettingsManager = None
    __recipe_manager: RecipeManager = None

    def __init__(self, reposity: DataReposity, settings_manager: SettingsManager, recipe_manager: RecipeManager) -> None:
        super().__init__()
        Validator.validate_type(reposity, DataReposity, 'reposity')
        Validator.validate_type(settings_manager, SettingsManager, 'settings_manager')
        Validator.validate_type(recipe_manager, RecipeManager, 'recipe_manager')
        self.__reposity = reposity
        self.__settings_manager = settings_manager
        self.__recipe_manager = recipe_manager

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> Settings:
        return self.__settings_manager.settings

    def __create_nomenclature_groups(self):
        list = []
        list.append(NomenclatureGroup.default_group_cold())
        list.append( NomenclatureGroup.default_group_source())
        self.__reposity.data[self.__reposity.group_key()] = list

    def __create_nomenclature(self):
        directory = f'files{os.sep}recipes'
        ingredients = []
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            self.__recipe_manager.open(file_path)
            recipe_ing = self.__recipe_manager.recipe.ingredients
            ingredients.append(recipe_ing)
            
        self.__reposity.data[self.__reposity.nomenclature_key()] = ingredients
            

    def __create_measurement_unit(self):
        kg_unit = MeasurementUnit.default_unit_kg()
        gramm_unit = MeasurementUnit.default_unit_gramm()
        thing_unit = MeasurementUnit.default_unit_thing()
        tablespoon_unit = MeasurementUnit.default_unit_tablespoon()
        teaspoon_unit = MeasurementUnit.default_unit_teaspoon()
        unit_list = (kg_unit, gramm_unit, thing_unit,
                     tablespoon_unit, teaspoon_unit)
        
        self.__reposity.data[self.__reposity.unit_key()] = unit_list
        
    def __create_receipts(self):
        recipe_files = ['waffles.md', 'chocolate_cookies.md']
        receipts_list = []
    
        for recipe_file in recipe_files:
            self.__recipe_manager.open(recipe_file)
            receipts_list.append(self.__recipe_manager.recipe)
    
        self.__reposity.data[self.__reposity.recipe_key()] = receipts_list

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurement_unit()
        self.__create_nomenclature()
        self.__create_receipts()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    


