import unittest
from datetime import datetime
from src.models.Warehouse import WarehouseModel
from src.models.Nomenclature import Nomenclature
from src.models.Measurement_unit import MeasurementUnit
from src.models.warehouse_transaction import WarehouseTransaction
from src.emuns.transaction_types import TransactionTypes
from general.exception.exceptions import ArgumentException

class TestWarehouseTransaction(unittest.TestCase):
    
    def setUp(self):
        """Set up test variables for each test."""
        self.warehouse = WarehouseModel(name="Test Warehouse", country="Test Country", city="Test City", street="Test Street", house_number="1")
        self.nomenclature = Nomenclature(name="Test Nomenclature", full_name="Test Full Nomenclature")
        self.unit = MeasurementUnit(name="Test Unit")
        self.count = 10.
        self.period = datetime.now()
        self.transaction_type = TransactionTypes.INCOME

    def test_initialization(self):
        """Test initialization of WarehouseTransaction with valid parameters."""
        transaction = WarehouseTransaction(
            warehouse=self.warehouse,
            nomenclature=self.nomenclature,
            count=self.count,
            unit=self.unit,
            period=self.period,
            transaction_type=self.transaction_type
        )
        
        self.assertEqual(transaction.warehouse, self.warehouse)
        self.assertEqual(transaction.nomenclature, self.nomenclature)
        self.assertEqual(transaction.count, self.count)
        self.assertEqual(transaction.unit, self.unit)
        self.assertEqual(transaction.period, self.period)
        self.assertEqual(transaction.transaction_type, self.transaction_type)

    def test_initialization_with_none(self):
        """Test initialization with None values."""
        transaction = WarehouseTransaction()
        
        self.assertIsInstance(transaction.warehouse, WarehouseModel)
        self.assertIsInstance(transaction.nomenclature, Nomenclature)
        self.assertEqual(transaction.count, 0)
        self.assertIsInstance(transaction.unit, MeasurementUnit)
        self.assertIsInstance(transaction.period, datetime)
        self.assertEqual(transaction.transaction_type, TransactionTypes.INCOME)

    def test_count_setter(self):
        """Test the count setter."""
        transaction = WarehouseTransaction()
        transaction.count = 20.0
        self.assertEqual(transaction.count, 20.0)
        

    def test_warehouse_setter(self):
        """Test the warehouse setter."""
        transaction = WarehouseTransaction()
        
        transaction.warehouse = self.warehouse
        self.assertEqual(transaction.warehouse, self.warehouse)
        
        with self.assertRaises(ArgumentException):
            transaction.warehouse = "Invalid Type"  # Should raise an exception

    def test_equality(self):
        """Test equality operator."""
        transaction1 = WarehouseTransaction(warehouse=self.warehouse, nomenclature=self.nomenclature, count=10., unit=self.unit, period=self.period)
        transaction2 = WarehouseTransaction(warehouse=self.warehouse, nomenclature=self.nomenclature, count=10., unit=self.unit, period=self.period)
        
        self.assertTrue(transaction1 == transaction2)
        
        transaction2.count = 20.
        self.assertFalse(transaction1 == transaction2)

