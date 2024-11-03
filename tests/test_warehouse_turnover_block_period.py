import unittest
from datetime import datetime, date

from src.models.warehouse_transaction import WarehouseTransaction
from src.models.warehouse_turnover import WarehouseTurnover

from src.emuns.transaction_types import TransactionTypes

from general.processors.process_warehouse_turnover_block_period import BlockPeriodTurnoverProcessor
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.data_reposity import DataReposity
from general.start_service import StartService

class TestBlockPeriodTurnoverProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up initial data and service for each test."""
        self.reposity = DataReposity()
        self.manager = SettingsManager()
        self.recipe_manager = RecipeManager()
        self.service = StartService(self.reposity, self.manager, self.recipe_manager)
        self.service.create()
        
        if not self.reposity.data[DataReposity.nomenclature_key()]:
            raise Exception("No data available!")

        # Define fixed test warehouses, nomenclature, and ranges
        self.warehouse_1 = self.reposity.data[DataReposity.warehouse_key()][0]
        self.warehouse_2 = self.reposity.data[DataReposity.warehouse_key()][1]
        self.nomenclature_1 = self.reposity.data[DataReposity.nomenclature_key()][0]
        self.nomenclature_2 = self.reposity.data[DataReposity.nomenclature_key()][1]
        self.range_1 = self.reposity.data[DataReposity.unit_key()][0]
        self.range_2 = self.reposity.data[DataReposity.unit_key()][1]

        # Create fixed transactions for testing
        self.transactions = [
            WarehouseTransaction(period=datetime(2024, 10, 23), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=100., transaction_type=TransactionTypes.INCOME),
            WarehouseTransaction(period=datetime(2024, 10, 30), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=50., transaction_type=TransactionTypes.EXPENSE),
            WarehouseTransaction(period=datetime(2024, 10, 1), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=25., transaction_type=TransactionTypes.EXPENSE),
            WarehouseTransaction(period=datetime(2024, 10, 20), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, unit=self.range_2, count=200., transaction_type=TransactionTypes.INCOME),
            WarehouseTransaction(period=datetime(2024, 10, 21), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, unit=self.range_2, count=100., transaction_type=TransactionTypes.EXPENSE),
        ]

    def test_turnover_with_default_block_period(self):
        """Test flow calculation with transactions within a specific period."""
        print("test 1")
        self.manager.settings.block_period = date(2024, 10, 1)
        process = BlockPeriodTurnoverProcessor()
        result = process.process(transactions=self.transactions)

        expected_turnovers = [
            WarehouseTurnover(warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, flow=-25.)
        ]

        self.assertEqual(len(result), len(expected_turnovers))
        for expected, actual in zip(expected_turnovers, result):
            self.assertEqual(expected.warehouse, actual.warehouse)
            self.assertEqual(expected.nomenclature, actual.nomenclature)
            self.assertEqual(expected.unit, actual.unit)
            self.assertEqual(expected.flow, actual.flow)
            
    def test_turnover_with_changed_block_period(self):
        """Test flow calculation with transactions within a specific period."""
        self.manager.settings.block_period = date(2024, 10, 22)
        process = BlockPeriodTurnoverProcessor()
        result = process.process(transactions=self.transactions)

        expected_turnovers = [
            WarehouseTurnover(warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, flow=75.),
        ]
        
        print(result[0].warehouse.name)
        self.assertEqual(len(result), len(expected_turnovers))
        for expected, actual in zip(expected_turnovers, result):
            self.assertEqual(expected.warehouse, actual.warehouse)
            self.assertEqual(expected.nomenclature, actual.nomenclature)
            self.assertEqual(expected.unit, actual.unit)
            self.assertEqual(expected.flow, actual.flow)