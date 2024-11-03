import unittest
import os
from datetime import datetime, date

from src.models.warehouse_transaction import WarehouseTransaction
from src.models.warehouse_turnover import WarehouseTurnover

from src.emuns.transaction_types import TransactionTypes

from general.processors.process_warehouse_turnover_block_period import BlockPeriodTurnoverProcessor
from general.processors.process_warehouse_turnover import WarehouseTurnoverProcess
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
        
        self.assertEqual(len(result), len(expected_turnovers))
        for expected, actual in zip(expected_turnovers, result):
            self.assertEqual(expected.warehouse, actual.warehouse)
            self.assertEqual(expected.nomenclature, actual.nomenclature)
            self.assertEqual(expected.unit, actual.unit)
            self.assertEqual(expected.flow, actual.flow)
            
    def test_load_turnover_calculation(self):
        """Load test for turnover calculation."""
        block_periods = [
            date(2024, 2, 1),
            date(2024, 6, 1),
            date(2024, 11, 1),
        ]

        results = {}

        for block_period in block_periods:
            elapsed_time = self.measure_time(block_period)
            results[block_period.strftime("%Y-%m-%d")] = elapsed_time
            
        dir_path = "test_files"
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, 'performance_results.md')
        
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write("# Результаты нагрузочного теста\n\n")
            f.write("| Дата блокировки | Время расчета (с) |\n")
            f.write("|------------------|-------------------|\n")
            for period, time in results.items():
                f.write(f"| {period} | {time:.4f} |\n")

    def measure_time(self, block_period):
        start_time = datetime.now()
        
        blocked_process = BlockPeriodTurnoverProcessor()
        self.manager.settings.block_period = block_period
        test_transactions = self.reposity.data[DataReposity.warehouse_transaction_key()]
        blocked_process.process(transactions=test_transactions)
        
        end_time = datetime.now()

        return (end_time - start_time).total_seconds()