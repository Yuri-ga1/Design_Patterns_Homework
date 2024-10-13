import unittest
from general.domain_prototype import DomainPrototype
from general.filter.filter_dto import FilterDTO
from general.filter.filter_matcher import FilterMatcher
from src.emuns.filter_types import FilterTypes

"""
Test suite for DomainPrototype and FilterDTO
"""
class TestDomainPrototype(unittest.TestCase):

    def setUp(self):
        # Setup test data
        self.data = [
            MockReference("Item1", "CODE1"),
            MockReference("Item2", "CODE2"),
            MockReference("Item3", "CODE3"),
        ]

    def test_prototype_filter_by_name_equals(self):
        """
        Test filtering DomainPrototype by name with EQUALS filter.
        """
        # Setup filter for exact match on name
        filt = FilterDTO(name="Item1", type_value=FilterTypes.EQUALS)
        prototype = DomainPrototype(self.data)

        # Perform the filtering
        result = prototype.create(self.data, filt)

        # Assertions
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].name, "Item1")

    def test_prototype_filter_by_unique_code_equals(self):
        """
        Test filtering DomainPrototype by unique_code with EQUALS filter.
        """
        # Setup filter for exact match on unique_code
        filt = FilterDTO(unique_code="CODE2", type_value=FilterTypes.EQUALS)
        prototype = DomainPrototype(self.data)

        # Perform the filtering
        result = prototype.create(self.data, filt)

        # Assertions
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].unique_code, "CODE2")

    def test_prototype_filter_by_name_like(self):
        """
        Test filtering DomainPrototype by name with LIKE filter.
        """
        # Setup filter for partial match on name
        filt = FilterDTO(name="Item", type_value=FilterTypes.LIKE)
        prototype = DomainPrototype(self.data)

        # Perform the filtering
        result = prototype.create(self.data, filt)

        # Assertions
        self.assertGreater(len(result.data), 0)
        self.assertTrue(all(item.name.startswith("Item") for item in result.data))

    def test_prototype_empty_filter(self):
        """
        Test filtering with an empty FilterDTO.
        """
        # Setup empty filter (should return all data)
        filt = FilterDTO()
        prototype = DomainPrototype(self.data)

        # Perform the filtering
        result = prototype.create(self.data, filt)

        # Assertions
        self.assertEqual(len(result.data), len(self.data))

class TestFilterMatcher(unittest.TestCase):

    def setUp(self):
        # Setup a FilterMatcher instance
        self.matcher = FilterMatcher()

    def test_match_equals(self):
        """
        Test matching fields using EQUALS filter.
        """
        field_value = "TestValue"
        filter_value = "TestValue"
        result = self.matcher.match_field(field_value, filter_value, FilterTypes.EQUALS)

        # Assertions
        self.assertTrue(result)

    def test_match_like(self):
        """
        Test matching fields using LIKE filter.
        """
        field_value = "TestValue"
        filter_value = "Test"
        result = self.matcher.match_field(field_value, filter_value, FilterTypes.LIKE)

        # Assertions
        self.assertTrue(result)

    def test_match_like_fail(self):
        """
        Test failing match using LIKE filter.
        """
        field_value = "TestValue"
        filter_value = "NoMatch"
        result = self.matcher.match_field(field_value, filter_value, FilterTypes.LIKE)

        # Assertions
        self.assertFalse(result)

# Mock class for AbstractReference to test DomainPrototype
class MockReference:
    def __init__(self, name, unique_code):
        self.name = name
        self.unique_code = unique_code

    def __eq__(self, other):
        if isinstance(other, MockReference):
            return self.name == other.name and self.unique_code == other.unique_code
        return False

if __name__ == '__main__':
    unittest.main()
