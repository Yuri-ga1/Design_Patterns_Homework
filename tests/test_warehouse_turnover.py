import unittest
from datetime import datetime, timedelta

from src.emuns.transaction_types import TransactionTypes

from src.models.warehouse_transaction import WarehouseTransaction
from src.models.warehouse_turnover import WarehouseTurnover

from general.processors.process_warehouse_turnover import WarehouseTurnoverProcess
from general.prototypes.warehouse_transaction_prototype import WarehouseTransactionPrototype
from general.data_reposity.data_reposity import DataReposity
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.start_service import StartService
from general.filter.filter_dto import FilterDTO
from general.filter.filter_warehouse_nomenclature_dto import WarehouseNomenclatureFilterDTO

class TestWarehouseTurnoverProcess(unittest.TestCase):
    
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
            WarehouseTransaction.create(period=datetime(2024, 10, 23), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=100., transaction_type=TransactionTypes.INCOME),
            WarehouseTransaction.create(period=datetime(2024, 10, 30), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=50., transaction_type=TransactionTypes.EXPENSE),
            WarehouseTransaction.create(period=datetime(2024, 10, 1), warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, count=25., transaction_type=TransactionTypes.EXPENSE),
            WarehouseTransaction.create(period=datetime(2024, 10, 20), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, unit=self.range_2, count=200., transaction_type=TransactionTypes.INCOME),
            WarehouseTransaction.create(period=datetime(2024, 10, 21), warehouse=self.warehouse_2, nomenclature=self.nomenclature_2, unit=self.range_2, count=100., transaction_type=TransactionTypes.EXPENSE),
        ]

    def test_turnover_within_period(self):
        """Test flow calculation with transactions within a specific period."""
        prototype = WarehouseTransactionPrototype(self.transactions)
        
        start_period = datetime(2024, 10, 22)
        end_period = datetime(2024, 10, 30)
        
        filt = WarehouseNomenclatureFilterDTO(start_period=start_period, end_period=end_period)
        filtered_data = prototype.create(self.transactions, filt)

        process = WarehouseTurnoverProcess()
        result = process.process(transactions=filtered_data.data)

        expected_turnovers = [
            WarehouseTurnover.create(warehouse=self.warehouse_1, nomenclature=self.nomenclature_1, unit=self.range_1, flow=100. - 50.)
        ]

        self.assertEqual(len(result), len(expected_turnovers))
        for expected, actual in zip(expected_turnovers, result):
            self.assertEqual(expected.warehouse, actual.warehouse)
            self.assertEqual(expected.nomenclature, actual.nomenclature)
            self.assertEqual(expected.unit, actual.unit)
            self.assertEqual(expected.flow, actual.flow)

    def test_turnover_without_filter(self):
        """Test flow calculation without any filters."""
        prototype = WarehouseTransactionPrototype(self.transactions)
        filtered_data = prototype.create(self.transactions, WarehouseNomenclatureFilterDTO())
        
        process = WarehouseTurnoverProcess()
        result = process.process(transactions=filtered_data.data)

        self.assertGreater(len(result), 0)

    def test_turnover_with_warehouse_filter(self):
        """Test flow calculation with a specific warehouse filter."""
        prototype = WarehouseTransactionPrototype(self.transactions)
        filt = WarehouseNomenclatureFilterDTO(warehouse=FilterDTO(name=self.warehouse_1.name))
        filtered_data = prototype.create(self.transactions, filt)

        process = WarehouseTurnoverProcess()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].warehouse, self.warehouse_1)

    def test_turnover_with_nomenclature_filter(self):
        """Test flow calculation with a specific nomenclature filter."""
        prototype = WarehouseTransactionPrototype(self.transactions)
        filt = WarehouseNomenclatureFilterDTO(nomenclature=FilterDTO(name=self.nomenclature_2.name))
        filtered_data = prototype.create(self.transactions, filt)

        process = WarehouseTurnoverProcess()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].nomenclature, self.nomenclature_2)

    def test_turnover_with_combined_filters(self):
        """Test flow calculation with combined filters for warehouse and nomenclature."""
        prototype = WarehouseTransactionPrototype(self.transactions)
        filt = WarehouseNomenclatureFilterDTO(
            warehouse=FilterDTO(name=self.warehouse_2.name),
            nomenclature=FilterDTO(name=self.nomenclature_2.name)
        )
        filtered_data = prototype.create(self.transactions, filt)

        process = WarehouseTurnoverProcess()
        result = process.process(transactions=filtered_data.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].warehouse, self.warehouse_2)
        self.assertEqual(result[0].nomenclature, self.nomenclature_2)

if __name__ == '__main__':
    unittest.main()
