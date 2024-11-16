import json
import os

from src.emuns.event_types import EventType
from general.abstract_files.abstract_manager import AbstractManager
from general.abstract_files.abstract_logic import AbstractLogic

from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.data_reposity.data_reposity import DataReposity
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.services.observe_service import ObserverService

from general.reports.report_factory import ReportFactory 
from src.emuns.format_reporting import FormatReporting

from general.deserializers.json_deserializer import JsonDeserializer

from general.start_service import StartService

class DataReposityManager(AbstractManager, AbstractLogic):
    __reposity: DataReposity = DataReposity()
    __service: StartService = None
    __save_folder = os.path.join('files', 'data_reposity')

    def __init__(self, settings_manager: SettingsManager, recipe_manager: RecipeManager) -> None:
        Validator.validate_type(settings_manager, SettingsManager, 'settings_manager')
        Validator.validate_type(recipe_manager, RecipeManager, 'recipe_manager')
        self.__settings_manager = settings_manager
        self.__service = StartService(
            reposity=self.__reposity,
            settings_manager=settings_manager,
            recipe_manager=recipe_manager,
        )
        ObserverService.add(self)
        
    
    def open(self, params):
        file_name = params['file_name']
        deserializer = JsonDeserializer()

        try:
            full_name = self._get_file_path(file_name)
            data = deserializer.deserialize(file_path=full_name)
            self.__reposity.data = data
            return True
        except Exception as e:
            self.set_exception(e)
            return False
        
    def save(self, params):
        file_name = params['file_name']

        data = self.__reposity.data
        
        result = {}
        for key, value in data.items():
            report = ReportFactory(self.__settings_manager).create(FormatReporting.JSON)
            report.create(value)
            result[key] = json.loads(report.result)

        
        os.makedirs(self.__save_folder, exist_ok=True)
        save_path = os.path.join(self.__save_folder, file_name)
        
        with open(save_path, 'w', encoding='utf-8') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=4)
            
    
    def _default_value(self):
        self.__service.create()
        ObserverService.raise_event(EventType.SAVE_SETTINGS, params=None)
        
    @property
    def reposity(self):
        return self.__reposity
    
    def set_exception(self, ex):
        self._inner_set_exception(ex)
    
    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)
        match type:
            case EventType.SAVE_REPOSITY:
                self.save(params)
            case EventType.LOAD_REPOSITY:
                self.open(params)
    