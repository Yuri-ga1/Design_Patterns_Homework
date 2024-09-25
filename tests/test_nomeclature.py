import unittest
from unittest.mock import Mock
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.models.Nomenclature import Nomenclature
from src.models.Nomeclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from general.exception.exceptions import *

class TestNomenclature(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.nomenclature = Nomenclature()
        self.mock_group = Mock(spec=NomenclatureGroup)
        self.mock_unit = Mock(spec=MeasurementUnit)
    
    def test_set_name_valid(self):
        """Тестирование установки корректного значения для name."""
        self.nomenclature.name = "Valid Name"
        self.assertEqual(self.nomenclature.name, "Valid Name")
    
    def test_set_name_invalid_type(self):
        """Тестирование установки некорректного типа для name."""
        with self.assertRaises(ArgumentException):
            self.nomenclature.name = 12345  # должно быть строкой
    
    def test_set_name_invalid_length(self):
        """Тестирование установки значения для name, которое слишком длинное."""
        long_name = "A" * 51  # Длина больше 50
        with self.assertRaises(MaxLengthException):
            self.nomenclature.name = long_name
    
    def test_set_full_name_valid(self):
        """Тестирование установки корректного значения для full_name."""
        self.nomenclature.full_name = "Valid Full Name"
        self.assertEqual(self.nomenclature.full_name, "Valid Full Name")
    
    def test_set_full_name_invalid_type(self):
        """Тестирование установки некорректного типа для full_name."""
        with self.assertRaises(ArgumentException):
            self.nomenclature.full_name = 12345  # должно быть строкой
    
    def test_set_full_name_invalid_length(self):
        """Тестирование установки значения для full_name, которое слишком длинное."""
        long_full_name = "A" * 256  # Длина больше 255
        with self.assertRaises(MaxLengthException):
            self.nomenclature.full_name = long_full_name
    
    def test_set_group_valid(self):
        """Тестирование установки корректного значения для group."""
        self.nomenclature.group = self.mock_group
        self.assertEqual(self.nomenclature.group, self.mock_group)
    
    def test_set_group_invalid_type(self):
        """Тестирование установки некорректного типа для group."""
        with self.assertRaises(ArgumentException):
            self.nomenclature.group = "Invalid Group"  # должно быть объектом NomenclatureGroup
    
    def test_set_unit_valid(self):
        """Тестирование установки корректного значения для unit."""
        self.nomenclature.unit = self.mock_unit
        self.assertEqual(self.nomenclature.unit, self.mock_unit)
    
    def test_set_unit_invalid_type(self):
        """Тестирование установки некорректного типа для unit."""
        with self.assertRaises(ArgumentException):
            self.nomenclature.unit = "Invalid Unit"  # должно быть объектом MeasurementUnit
