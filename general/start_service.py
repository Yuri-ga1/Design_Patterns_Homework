import os

from general.abstract_files.abstract_logic import AbstractLogic
from general.data_reposity import data_reposity
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from general.settings.settings_manager import SettingsManager
from general.settings.settings import Settings
from general.recipes.recipe_manager import RecipeManager

from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomeclature_group import NomenclatureGroup


"""
Сервис для реализации первого старта приложения
"""
class start_service(AbstractLogic):
    __reposity: data_reposity = None
    __settings_manager: SettingsManager = None

    def __init__(self, reposity: data_reposity, manager: SettingsManager ) -> None:
        super().__init__()
        Validator.validate_type(reposity, data_reposity, 'reposity')
        Validator.validate_type(manager, SettingsManager, 'manager')
        self.__reposity = reposity
        self.__settings_manager = manager

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
        self.__reposity.data[data_reposity.group_key()] = list

    def __create_nomenclature(self):
        directory = f'files{os.sep}recipes'
        ingredients = []
        recipe_manager = RecipeManager()
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            recipe_manager.open(file_path)
            recipe_ing = recipe_manager.recipe.ingredients.keys()
            ingredients.append(recipe_ing)
            
        self.__reposity.data[data_reposity.nomenclature_key()] = ingredients
            

    def __create_measurement_unit(self):
        kg_unit = MeasurementUnit("Килограмм")
        gramm_unit = MeasurementUnit("Грамм", kg_unit, 1000)
        thing_unit = MeasurementUnit("Штука")
        tablespoon_unit = MeasurementUnit("Столовая ложка")
        teaspoon_unit = MeasurementUnit("Чайная ложка", tablespoon_unit, 3)
        unit_list = (kg_unit, gramm_unit, thing_unit,
                     tablespoon_unit, teaspoon_unit)
        
        self.__reposity.data[data_reposity.unit_key()] = unit_list
        
    def __create_receipts(self):
        pass

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurement_unit()
        self.__create_nomenclature()
        self.__create_receipts()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    


