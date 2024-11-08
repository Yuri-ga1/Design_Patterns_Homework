import unittest
from general.start_service import StartService
from general.data_reposity import DataReposity
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager

class TestDataRepository(unittest.TestCase):

    def setUp(self):
        self.reposity = DataReposity()
        self.settings_manager = SettingsManager()
        self.recipe_manager = RecipeManager()
        self.service = StartService(self.reposity, self.settings_manager, self.recipe_manager)
        
        
    def test_data_created(self):
        self.service.create()

        keys_to_check = {
            DataReposity.nomenclature_key(): 0,
            DataReposity.group_key(): 0,
            DataReposity.unit_key(): 0,
            DataReposity.recipe_key(): 0,
            DataReposity.warehouse_key(): 0,
            DataReposity.warehouse_transaction_key(): 0,
        }
    
        for key, min_length in keys_to_check.items():
            self.assertTrue(key in self.reposity.data, f"{key} отсутствует в данных")
            self.assertGreater(len(self.reposity.data[key]), min_length, f"Размер данных для {key} меньше ожидаемого")
