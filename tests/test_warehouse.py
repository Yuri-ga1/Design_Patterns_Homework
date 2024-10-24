import unittest
from src.models.Warehouse import WarehouseModel

class TestWarehouseModel(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.warehouse = WarehouseModel()

    def test_set_name_valid(self):
        """Тестирование установки корректного значения для name."""
        self.warehouse.name = "Main Warehouse"
        self.assertEqual(self.warehouse.name, "Main Warehouse")

    def test_set_country_valid(self):
        """Тестирование установки корректного значения для country."""
        self.warehouse.country = "USA"
        self.assertEqual(self.warehouse.country, "USA")

    def test_set_city_valid(self):
        """Тестирование установки корректного значения для city."""
        self.warehouse.city = "New York"
        self.assertEqual(self.warehouse.city, "New York")

    def test_set_street_valid(self):
        """Тестирование установки корректного значения для street."""
        self.warehouse.street = "5th Avenue"
        self.assertEqual(self.warehouse.street, "5th Avenue")

    def test_set_house_number_valid(self):
        """Тестирование установки корректного значения для house_number."""
        self.warehouse.house_number = "123A"
        self.assertEqual(self.warehouse.house_number, "123A")

    def test_set_fields_with_whitespace(self):
        """Тестирование удаления лишних пробелов для всех полей."""
        self.warehouse.name = "  Main Warehouse  "
        self.warehouse.country = "  USA  "
        self.warehouse.city = "  New York  "
        self.warehouse.street = "  5th Avenue  "
        self.warehouse.house_number = "  123A  "
        self.assertEqual(self.warehouse.name, "Main Warehouse")
        self.assertEqual(self.warehouse.country, "USA")
        self.assertEqual(self.warehouse.city, "New York")
        self.assertEqual(self.warehouse.street, "5th Avenue")
        self.assertEqual(self.warehouse.house_number, "123A")

    def test_equality_same_address(self):
        """Тестирование оператора равенства для объектов с одинаковыми данными."""
        other_warehouse = WarehouseModel(
            name="Main Warehouse",
            country="USA",
            city="New York",
            street="5th Avenue",
            house_number="123A"
        )
        self.warehouse.name = "Main Warehouse"
        self.warehouse.country = "USA"
        self.warehouse.city = "New York"
        self.warehouse.street = "5th Avenue"
        self.warehouse.house_number = "123A"
        self.assertEqual(self.warehouse, other_warehouse)

    def test_equality_different_address(self):
        """Тестирование оператора равенства для объектов с разными данными."""
        other_warehouse = WarehouseModel(
            name="Secondary Warehouse",
            country="Canada",
            city="Toronto",
            street="Queen St",
            house_number="456"
        )
        self.warehouse.name = "Main Warehouse"
        self.warehouse.country = "USA"
        self.warehouse.city = "New York"
        self.warehouse.street = "5th Avenue"
        self.warehouse.house_number = "123A"
        self.assertNotEqual(self.warehouse, other_warehouse)
