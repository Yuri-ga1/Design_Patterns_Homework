import unittest
from unittest.mock import patch, mock_open
from settings.settings_manager import SettingsManager
from settings.models.Settings import Settings
from general.exception.exceptions import ArgumentException


class TestSettingsManager(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.manager = SettingsManager()

   
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.isfile", return_value=False)
    def test_open_file_not_found(self, mock_isfile, mock_open_file):
        """Тестирование обработки отсутствующего файла настроек."""
        result = self.manager.open("non_existent_file.json")
        self.assertFalse(result)
        self.assertEqual(self.manager.settings.inn, "012345678901")
        self.assertEqual(self.manager.settings.organization_name, "Рога и копыта (default)")

    
    @patch("os.walk", return_value=[(".", [], ["settings.json"])])
    def test_get_file_path_file_not_found(self, mock_walk):
        """Тестирование поиска файла, когда файл не найден."""
        result = self.manager._SettingsManager__get_file_path("non_existent_file.json")
        self.assertIsNone(result)

    def test_default_settings(self):
        """Тестирование настройки по умолчанию."""
        default_settings = self.manager._SettingsManager__default_settings()
        self.assertEqual(default_settings.inn, "012345678901")
        self.assertEqual(default_settings.organization_name, "Рога и копыта (default)")
        self.assertEqual(default_settings.account, "01234567890")
        self.assertEqual(default_settings.correspondent_account, "01234567890")
        self.assertEqual(default_settings.bic, "012345678")
        self.assertEqual(default_settings.property_type, "01234")
