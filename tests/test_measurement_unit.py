import unittest
from unittest.mock import Mock
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from src.models.Measurement_unit import MeasurementUnit
from general.exception.exceptions import ArgumentException, MaxLengthException


class TestMeasurementUnit(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.measurement_unit = MeasurementUnit()
        self.mock_unit = Mock(spec=MeasurementUnit)

    def test_set_name_valid(self):
        """Тестирование установки корректного значения для name."""
        self.measurement_unit.name = "Valid Name"
        self.assertEqual(self.measurement_unit.name, "Valid Name")

    def test_set_name_invalid_type(self):
        """Тестирование установки некорректного типа для name."""
        with self.assertRaises(ArgumentException):
            self.measurement_unit.name = 12345  # должно быть строкой

    def test_set_name_invalid_length(self):
        """Тестирование установки значения для name, которое слишком длинное."""
        long_name = "A" * 51  # Длина больше 50
        with self.assertRaises(MaxLengthException):
            self.measurement_unit.name = long_name

    def test_set_base_unit_valid(self):
        """Тестирование установки корректного значения для unit и conversion_rate."""
        self.measurement_unit.set_base_unit(self.mock_unit, 10)
        self.assertEqual(self.measurement_unit.unit, self.mock_unit)
        self.assertEqual(self.measurement_unit.conversion_rate, 10)

    def test_set_base_unit_invalid_type(self):
        """Тестирование установки некорректного типа для unit."""
        with self.assertRaises(ArgumentException):
            self.measurement_unit.set_base_unit("Invalid Unit", 10)  # unit должен быть объектом MeasurementUnit

    def test_set_base_unit_invalid_conversion_rate_type(self):
        """Тестирование установки некорректного типа для conversion_rate."""
        with self.assertRaises(ArgumentException):
            self.measurement_unit.set_base_unit(self.mock_unit, "Invalid Conversion Rate")  # должно быть int
