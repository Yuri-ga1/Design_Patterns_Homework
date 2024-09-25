from general.abstract_files.abstract_logic import AbstractLogic
from general.abstract_files.abstract_report import AbstractReport
from src.emuns.format_reporting import FormatReporting

from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.settings.settings_manager import SettingsManager

"""
Фабрика для формирования отчетов
"""
class ReportFactory(AbstractLogic):
    __reports = {}

    def __init__(self, settings_manager: SettingsManager = SettingsManager()) -> None:
        super().__init__()
        Validator.validate_type(settings_manager, SettingsManager, "setting_manager")
        self.__settings_manager = settings_manager
        self._load_reports()
        
        
    def _load_reports(self) -> None:
        """Загружает все отчеты динамически из папки formats."""
        
        report_module_base = 'general.reports.formats'

        for report_format in FormatReporting:
            module_name = report_format.name.lower() + '_report'
            class_name = report_format.name.capitalize() + 'Report'

            module = Validator.validate_module_exists(f'{report_module_base}.{module_name}', report_format.name)
            report_class = Validator.validate_class_exists(module, class_name, report_format.name)
            
            self.__reports[report_format] = report_class

    def create_default(self) -> AbstractReport:
        """Создает отчет в зависимости от загруженных настроек."""
        default_report = self.__settings_manager.settings.default_report_format
        default_enum = FormatReporting[default_report.upper()]
        
        if default_enum in self.__reports:
            return self.create(default_enum)


    def create(self, format: FormatReporting) ->  AbstractReport: 
        Validator.validate_type(format, FormatReporting, 'format')
        Validator.validate_format(format, self.__reports.keys())
        
        report = self.__reports[format]
        return report()
    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
       