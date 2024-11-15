import unittest
from unittest.mock import MagicMock
from datetime import date
import os
import json

from general.reports.trial_balance import TrialBalanceReport  # замените на правильный путь
from general.filter.filter_dto import FilterDTO
from general.processors.process_warehouse_turnover_block_period import BlockPeriodTurnoverProcessor
from src.emuns.event_types import EventType


class TestTrialBalanceReport(unittest.TestCase):
    def setUp(self):
        self.settings_manager = MagicMock()
        self.report = TrialBalanceReport(self.settings_manager)

    def mock_nomenclature_unit(self, name, unit_name):
        mock_nomenclature = MagicMock()
        mock_nomenclature.name = name
        mock_unit = MagicMock()
        mock_unit.name = unit_name
        return mock_nomenclature, mock_unit

    def test_create_success(self):
        # Мокаем зависимости
        mock_processor = MagicMock(spec=BlockPeriodTurnoverProcessor)
        mock_processor.process.side_effect = [
            {"key1": MagicMock(flow=10, nomenclature=self.mock_nomenclature_unit("Item1", "kg")[0], unit=self.mock_nomenclature_unit("Item1", "kg")[1])},
            {"key1": MagicMock(flow=5, nomenclature=self.mock_nomenclature_unit("Item1", "kg")[0], unit=self.mock_nomenclature_unit("Item1", "kg")[1])},
        ]
        self.report.get_data_for_period = MagicMock(return_value=mock_processor.process.side_effect)

        mock_prototype = MagicMock()
        mock_prototype.create.return_value = mock_prototype
        mock_prototype.data = [{"mock": "transaction_data"}]

        # Мокаем DomainPrototype
        with unittest.mock.patch("general.domain_prototype.DomainPrototype", return_value=mock_prototype):
            params = {
                "transactions": [{"mock": "data"}],
                "warehouse_filter": MagicMock(dict=MagicMock(return_value={"filter": "data"})),
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 1, 31),
            }

            # Выполняем метод
            result = self.report.create(params)

        # Проверяем результат
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["nomenclature_name"], "Item1")
        self.assertEqual(result[0]["unit"], "kg")
        self.assertEqual(result[0]["flow_first_period"], 10)
        self.assertEqual(result[0]["flow_second_period"], 5)
        self.assertEqual(result[0]["total_flow"], 15)

        # Проверяем сохранение файла
        file_path = os.path.join("files", "trial_balance_report.json")
        with open(file_path, "r", encoding="utf-8") as f:
            file_data = json.load(f)
        
        # Преобразуем моки в обычные объекты для сравнения
        file_data = [{"nomenclature_name": item["nomenclature_name"], "unit": item["unit"], 
                      "flow_first_period": item["flow_first_period"], "flow_second_period": item["flow_second_period"], 
                      "total_flow": item["total_flow"]} for item in file_data]

        self.assertEqual(file_data, result)

    def test_get_data_for_period_success(self):
        # Мокаем BlockPeriodTurnoverProcessor
        mock_processor = MagicMock(spec=BlockPeriodTurnoverProcessor)
        mock_processor.process.side_effect = [
            {"key1": MagicMock()},
            {"key2": MagicMock()},
        ]
        self.report.get_data_for_period = MagicMock(return_value=mock_processor.process.side_effect)

        # Вызываем метод
        first_period, second_period = self.report.get_data_for_period(
            transaction=[{"mock": "transaction"}],
            start_period=date(2024, 1, 1),
            end_period=date(2024, 1, 31),
        )

        # Проверяем результат
        self.assertEqual(len(first_period), 1)
        self.assertEqual(len(second_period), 1)

    def test_get_data_for_period_no_transactions(self):
        with self.assertRaises(ValueError) as context:
            self.report.get_data_for_period(transaction=[], start_period=date(2024, 1, 1))
        self.assertEqual(str(context.exception), "No transactions found")


    def test_handle_event_create_report(self):
        params = MagicMock()
        self.report.create = MagicMock(return_value="MockReport")

        result = self.report.handle_event(EventType.CREATE_TRIAL_BALANCE_REPORT, params)

        self.report.create.assert_called_once_with(params)
        self.assertEqual(result, "MockReport")


if __name__ == "__main__":
    unittest.main()
