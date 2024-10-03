import unittest
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.models.Nomenclature_group import NomenclatureGroup
from general.exception.exceptions import ArgumentException, MaxLengthException


class TestNomenclatureGroup(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.nomenclature_group = NomenclatureGroup()

    def test_set_name_valid(self):
        """Тестирование установки корректного значения для name."""
        self.nomenclature_group.name = "Valid Name"
        self.assertEqual(self.nomenclature_group.name, "Valid Name")

    def test_set_name_invalid_type(self):
        """Тестирование установки некорректного типа для name."""
        with self.assertRaises(ArgumentException):
            self.nomenclature_group.name = 12345  # должно быть строкой

    def test_set_name_invalid_length(self):
        """Тестирование установки значения для name, которое слишком длинное."""
        long_name = "A" * 51  # Длина больше 50
        with self.assertRaises(MaxLengthException):
            self.nomenclature_group.name = long_name

    def test_equality_same_name(self):
        """Тестирование оператора равенства для объектов с одинаковым именем."""
        other_group = NomenclatureGroup()
        self.nomenclature_group.name = "Same Name"
        other_group.name = "Same Name"
        self.assertEqual(self.nomenclature_group, other_group)

    def test_equality_different_name(self):
        """Тестирование оператора равенства для объектов с разными именами."""
        other_group = NomenclatureGroup()
        self.nomenclature_group.name = "Name One"
        other_group.name = "Name Two"
        self.assertNotEqual(self.nomenclature_group, other_group)
