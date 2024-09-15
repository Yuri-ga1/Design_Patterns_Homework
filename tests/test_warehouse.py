import unittest
from src.models.Warehouse import WarehouseModel


class TestWarehouseModel(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.warehouse = WarehouseModel()

    def test_set_address_valid(self):
        """Тестирование установки корректного значения для address."""
        self.warehouse.address = "123 Main Street"
        self.assertEqual(self.warehouse.address, "123 Main Street")

    def test_set_address_with_whitespace(self):
        """Тестирование удаления лишних пробелов в начале и в конце address."""
        self.warehouse.address = "  456 Secondary St  "
        self.assertEqual(self.warehouse.address, "456 Secondary St")

    def test_equality_same_address(self):
        """Тестирование оператора равенства для объектов с одинаковым address."""
        other_warehouse = WarehouseModel()
        self.warehouse.address = "789 Warehouse Rd"
        other_warehouse.address = "789 Warehouse Rd"
        self.assertEqual(self.warehouse, other_warehouse)

    def test_equality_different_address(self):
        """Тестирование оператора равенства для объектов с разными address."""
        other_warehouse = WarehouseModel()
        self.warehouse.address = "123 Main St"
        other_warehouse.address = "456 Elm St"
        self.assertNotEqual(self.warehouse, other_warehouse)
