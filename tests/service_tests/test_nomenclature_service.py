import unittest
from unittest.mock import MagicMock, patch
from general.services.nomenclature_service import NomenclatureService
from general.data_reposity import DataReposity
from src.models.Nomenclature import Nomenclature
from general.filter.filter_dto import FilterDTO

class TestNomenclatureService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=DataReposity)
        self.service = NomenclatureService(self.mock_repository)

    def test_add_nomenclature_success(self):
        self.service.get_group_by_id = MagicMock(return_value="MockGroup")
        self.service.get_unit_by_id = MagicMock(return_value="MockUnit")
        self.mock_repository[DataReposity.nomenclature_key()] = []

        result = self.service.add("TestName", "TestFullName", "GroupID", "UnitID")

        self.assertEqual(result, {"message": "New nomenclature add successfully"})
        self.assertEqual(len(self.mock_repository[DataReposity.nomenclature_key()]), 1)

    def test_add_nomenclature_group_not_exist(self):
        self.service.get_group_by_id = MagicMock(return_value=None)
        result = self.service.add("TestName", "TestFullName", "InvalidGroupID", "UnitID")
        self.assertEqual(result, {"message": "Group with id InvalidGroupID is not exist"})

    def test_add_nomenclature_unit_not_exist(self):
        self.service.get_group_by_id = MagicMock(return_value="MockGroup")
        self.service.get_unit_by_id = MagicMock(return_value=None)
        result = self.service.add("TestName", "TestFullName", "GroupID", "InvalidUnitID")
        self.assertEqual(result, {"message": "Unit with id InvalidUnitID is not exist"})

    def test_get_nomenclature_found(self):
        mock_nomenclature = MagicMock()
        self.service.filter_data = MagicMock(return_value=[mock_nomenclature])
        result = self.service.get("UniqueCode")
        self.assertEqual(result, mock_nomenclature)

    def test_get_nomenclature_not_found(self):
        self.service.filter_data = MagicMock(return_value=[])
        result = self.service.get("NonexistentCode")
        self.assertIsNone(result)

    def test_update_nomenclature_success(self):
        mock_nomenclature = MagicMock()
        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.update_nomenclature = MagicMock()
        self.service.update_nomenclature_in_recipes = MagicMock()
        self.service.update_nomenclature_in_transactions = MagicMock()

        result = self.service.update("UniqueCode", "UpdatedName", "UpdatedFullName", "GroupID", "UnitID")
        
        self.assertEqual(result, {"message": f"Nomenclature with id UniqueCode updated successfully"})
        self.service.update_nomenclature.assert_called_once_with(mock_nomenclature, {
            'name': "UpdatedName",
            'full_name': "UpdatedFullName",
            'group_id': "GroupID",
            'unit_id': "UnitID"
        })

    def test_update_nomenclature_not_exist(self):
        self.service.get = MagicMock(return_value=None)
        result = self.service.update("InvalidCode", "Name", "FullName", "GroupID", "UnitID")
        self.assertEqual(result, {"message": f"Nomenclature with id InvalidCode is not exist"})

    def test_delete_nomenclature_success(self):
        mock_nomenclature = MagicMock()
        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.is_in_recipes = MagicMock(return_value=False)
        self.service.is_in_transaction = MagicMock(return_value=False)
        self.mock_repository[DataReposity.nomenclature_key()] = [mock_nomenclature]

        result = self.service.delete("UniqueCode")
        self.assertEqual(result, {"message": f"Nomenclature with id UniqueCode successfully deleted"})

    def test_delete_nomenclature_in_use(self):
        mock_nomenclature = MagicMock()
        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.is_in_recipes = MagicMock(return_value=True)
        result = self.service.delete("UniqueCode")
        self.assertEqual(result, {"message": f"Nomenclature with id UniqueCode used in recipes or in transactions"})

    def test_filter_data(self):
        self.mock_repository.data = {
            DataReposity.nomenclature_key(): ["MockNomenclatureData"]
        }
        filter_dto = FilterDTO(unique_code="UniqueCode")
        with patch("general.domain_prototype.DomainPrototype") as MockPrototype:
            mock_prototype = MockPrototype.return_value
            mock_prototype.create.return_value = mock_prototype
            mock_prototype.data = ["FilteredData"]
            result = self.service.filter_data(filter_dto)
            self.assertEqual(result, ["FilteredData"])

if __name__ == '__main__':
    unittest.main()
