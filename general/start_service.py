from general.abstract_files.abstract_logic import AbstractLogic
from general.data_reposity import data_reposity
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.models.Nomeclature_group import NomenclatureGroup
from general.settings.settings_manager import SettingsManager
from general.settings.models.Settings import Settings

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

    """
    Сформировать группы номенклатуры
    """
    def __create_nomenclature_groups(self):
        list = []
        list.append(NomenclatureGroup.default_group_cold())
        list.append( NomenclatureGroup.default_group_source())
        self.__reposity.data[data_reposity.group_key()] = list    

    """
    Первый старт
    """
    def create(self):
        self.__create_nomenclature_groups()


    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    


