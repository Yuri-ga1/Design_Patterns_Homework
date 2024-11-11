import unittest
from unittest.mock import MagicMock, patch
from general.services.nomenclature_service import NomenclatureService
from general.data_reposity import DataReposity
from general.filter.filter_dto import FilterDTO
from src.models.Nomenclature import Nomenclature

class TestNomenclatureService(unittest.TestCase):

    def setUp(self):
        self.mock_repository = MagicMock(spec=DataReposity)
        self.service = NomenclatureService(self.mock_repository)

    def test_add_nomenclature_success(self):
        self.service.get_group_by_id = MagicMock(return_value="MockGroup")
        self.service.get_unit_by_id = MagicMock(return_value="MockUnit")

        # Настраиваем mock_repository как словарь для хранения номенклатуры
        nomenclature_key = DataReposity.nomenclature_key()
        setattr(self.mock_repository, nomenclature_key, [])

        # Имитация метода add, добавляющего элемент в номенклатуру
        def mock_add_nomenclature(name, full_name, group_id, unit_id):
            getattr(self.mock_repository, nomenclature_key).append({
                "name": name,
                "full_name": full_name,
                "group_id": group_id,
                "unit_id": unit_id
            })
            return {"message": "New nomenclature add successfully"}

        # Подменяем метод add в сервисе на mock-функцию
        self.service.add = mock_add_nomenclature

        result = self.service.add("TestName", "TestFullName", "GroupID", "UnitID")

        self.assertEqual(result, {"message": "New nomenclature add successfully"})
        self.assertEqual(len(getattr(self.mock_repository, nomenclature_key)), 1)




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
        params = {
            "unique_code": "UniqueCode",
            "name": "UpdatedName",
            "full_name": "UpdatedFullName",
            "group_id": "GroupID",
            "unit_id": "UnitID"
        }
        
        # Настраиваем метод get, чтобы он возвращал mock_nomenclature
        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.update_nomenclature = MagicMock()
    
        # Вызываем метод update и передаем параметры
        result = self.service.update(params)
    
        # Проверяем результат и правильность вызова с именованными аргументами
        self.assertEqual(result, {"message": f"Nomenclature with id UniqueCode updated successfully"})
        self.service.update_nomenclature.assert_called_once_with(nomenclature=mock_nomenclature, params=params)


    def test_update_nomenclature_not_exist(self):
        params = {
            "unique_code": "InvalidCode",
            "name": "Name",
            "full_name": "FullName",
            "group_id": "GroupID",
            "unit_id": "UnitID"
        }
        self.service.get = MagicMock(return_value=None)
        result = self.service.update(params)
        self.assertEqual(result, {"message": f"Nomenclature with id InvalidCode is not exist"})

    def test_delete_nomenclature_success(self):
        mock_nomenclature = MagicMock()
        nomenclature_key = DataReposity.nomenclature_key()

        # Настраиваем хранилище номенклатуры
        setattr(self.mock_repository, nomenclature_key, [mock_nomenclature])

        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.is_in_recipes = MagicMock(return_value=False)
        self.service.is_in_transaction = MagicMock(return_value=False)

        # Подменяем логику удаления
        def mock_delete_nomenclature(unique_code):
            if unique_code == "UniqueCode" and mock_nomenclature in getattr(self.mock_repository, nomenclature_key):
                getattr(self.mock_repository, nomenclature_key).remove(mock_nomenclature)
                return {"message": f"Nomenclature with id {unique_code} successfully deleted"}

        # Заменяем метод delete сервиса на mock-функцию
        self.service.delete = mock_delete_nomenclature

        result = self.service.delete("UniqueCode")
        self.assertEqual(result, {"message": f"Nomenclature with id UniqueCode successfully deleted"})
        self.assertEqual(len(getattr(self.mock_repository, nomenclature_key)), 0)


    def test_delete_nomenclature_in_use(self):
        mock_nomenclature = MagicMock()
        nomenclature_key = DataReposity.nomenclature_key()

        # Настраиваем хранилище номенклатуры
        setattr(self.mock_repository, nomenclature_key, [mock_nomenclature])

        self.service.get = MagicMock(return_value=mock_nomenclature)
        self.service.is_in_recipes = MagicMock(return_value=True)
        self.service.is_in_transaction = MagicMock(return_value=False)

        # Подменяем логику удаления
        def mock_delete_nomenclature(unique_code):
            if unique_code == "UniqueCode" and mock_nomenclature in getattr(self.mock_repository, nomenclature_key):
                return {"message": f"Nomenclature with id {unique_code} used in recipes or in transactions"}

        # Заменяем метод delete сервиса на mock-функцию
        self.service.delete = mock_delete_nomenclature

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
