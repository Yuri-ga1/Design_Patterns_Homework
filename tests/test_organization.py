import unittest
from unittest.mock import Mock
from src.models.Organization import Organization
from settings.models.Settings import Settings
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.exception.exceptions import ArgumentException, LengthException, DigitsException


class TestOrganization(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.organization = Organization()
    
    def test_set_inn_valid(self):
        """Тестирование установки корректного значения для INN."""
        self.organization.inn = "123456789012"  # 12 символов
        self.assertEqual(self.organization.inn, "123456789012")
    
    def test_set_inn_invalid_type(self):
        """Тестирование установки некорректного типа для INN."""
        with self.assertRaises(ArgumentException):
            self.organization.inn = 123456789012  # Должно быть строкой
    
    def test_set_inn_invalid_length(self):
        """Тестирование установки значения для INN, которое имеет некорректную длину."""
        with self.assertRaises(LengthException):
            self.organization.inn = "12345678901"  # Меньше 12 символов
    
    def test_set_account_valid(self):
        """Тестирование установки корректного значения для account."""
        self.organization.account = "12345678901"  # 11 символов
        self.assertEqual(self.organization.account, "12345678901")
    
    def test_set_account_invalid_type(self):
        """Тестирование установки некорректного типа для account."""
        with self.assertRaises(ArgumentException):
            self.organization.account = 12345678901  # Должно быть строкой
    
    def test_set_account_invalid_digits(self):
        """Тестирование установки некорректного значения для account (не все цифры)."""
        with self.assertRaises(DigitsException):
            self.organization.account = "12345abc901"  # Должны быть только цифры
    
    def test_set_bic_valid(self):
        """Тестирование установки корректного значения для BIC."""
        self.organization.bic = "123456789"  # 9 символов
        self.assertEqual(self.organization.bic, "123456789")
    
    def test_set_bic_invalid_type(self):
        """Тестирование установки некорректного типа для BIC."""
        with self.assertRaises(ArgumentException):
            self.organization.bic = 123456789  # Должно быть строкой
    
    def test_set_bic_invalid_digits(self):
        """Тестирование установки некорректного значения для BIC (не все цифры)."""
        with self.assertRaises(DigitsException):
            self.organization.bic = "12345abc9"  # Должны быть только цифры
    
    def test_set_property_type_valid(self):
        """Тестирование установки корректного значения для property_type."""
        self.organization.property_type = "123456789"  # 9 символов
        self.assertEqual(self.organization.property_type, "123456789")
    
    def test_set_property_type_invalid_type(self):
        """Тестирование установки некорректного типа для property_type."""
        with self.assertRaises(ArgumentException):
            self.organization.property_type = 12345  # Должно быть строкой
    
    def test_set_property_type_invalid_length(self):
        """Тестирование установки некорректного значения для property_type (некорректная длина)."""
        with self.assertRaises(LengthException):
            self.organization.property_type = "1234"  # Меньше 9 символов
    
    def test_load_settings(self):
        """Тестирование загрузки настроек из Settings."""
        mock_settings = Mock(spec=Settings)
        mock_settings.inn = "123456789012"
        mock_settings.account = "12345678901"
        mock_settings.bic = "123456789"
        mock_settings.property_type = "123456789"

        self.organization.load_settings(mock_settings)
        
        self.assertEqual(self.organization.inn, "123456789012")
        self.assertEqual(self.organization.account, "12345678901")
        self.assertEqual(self.organization.bic, "123456789")
        self.assertEqual(self.organization.property_type, "123456789")
    
    def test_equality(self):
        """Тестирование сравнения двух объектов Organization."""
        other = Organization()
        other.inn = "123456789012"
        other.account = "12345678901"
        other.bic = "123456789"
        other.property_type = "123456789"
        
        self.organization.inn = "123456789012"
        self.organization.account = "12345678901"
        self.organization.bic = "123456789"
        self.organization.property_type = "123456789"
        
        self.assertTrue(self.organization == other)
