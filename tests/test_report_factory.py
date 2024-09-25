import unittest
from unittest.mock import patch, MagicMock
from general.reports.report_factory import ReportFactory
from src.emuns.format_reporting import FormatReporting
from general.exception.exceptions import ArgumentException, NotFoundException

class TestReportFactory(unittest.TestCase):

    @patch('general.settings.settings_manager.SettingsManager')
    @patch('general.exception.Validator_wrapper.ValidatorWrapper')
    def setUp(self, MockValidator, MockSettingsManager):
        """Настройка перед каждым тестом."""
        # Настройка заглушки для настроек
        MockSettingsManager.settings.default_report_format = 'CSV'
        self.factory = ReportFactory()

        # Создаем заглушки для классов отчетов
        self.mock_csv_report = MagicMock(name='CsvReport')
        self.mock_json_report = MagicMock(name='JsonReport')
        
        # Настройка загрузки отчетов
        self.factory._ReportFactory__reports = {
            FormatReporting.CSV: self.mock_csv_report,
            FormatReporting.JSON: self.mock_json_report
        }

    def test_load_reports(self):
        """Проверяет, что отчеты загружаются корректно."""
        self.assertIn(FormatReporting.CSV, self.factory._ReportFactory__reports)
        self.assertIn(FormatReporting.JSON, self.factory._ReportFactory__reports)

    def test_create_report(self):
        """Проверяет создание отчета по формату."""
        report = self.factory.create(FormatReporting.CSV)
        self.assertIsInstance(report, MagicMock)
        report = self.factory.create(FormatReporting.JSON)
        self.assertIsInstance(report, MagicMock)

    def test_create_default_report(self):
        """Проверяет создание отчета по умолчанию."""
        report = self.factory.create_default()
        self.assertIsInstance(report, MagicMock)  # Ожидается, что это будет заглушка для CsvReport

    @patch('general.exception.Validator_wrapper.ValidatorWrapper.validate_format')
    def test_create_default_report_invalid_format(self, mock_validate_format):
        """Проверяет исключение при некорректном формате отчета по умолчанию."""
        mock_validate_format.side_effect = ValueError('Invalid format')
        with self.assertRaises(ValueError):
            self.factory.create_default()

    @patch('general.exception.Validator_wrapper.ValidatorWrapper.validate_format')
    def test_create_report_invalid_format(self, mock_validate_format):
        """Проверяет исключение при некорректном формате отчета."""
        mock_validate_format.side_effect = ArgumentException('format', 'Invalid format')
        with self.assertRaises(ArgumentException):
            self.factory.create(FormatReporting.CSV)  # Используем существующий формат для теста

    @patch('general.exception.Validator_wrapper.ValidatorWrapper.validate_format')
    def test_create_report_not_found(self, mock_validate_format):
        """Проверяет исключение при отсутствии формата."""
        mock_validate_format.side_effect = NotFoundException()
        with self.assertRaises(NotFoundException):
            self.factory.create(FormatReporting.JSON)  # Используем существующий формат для теста
