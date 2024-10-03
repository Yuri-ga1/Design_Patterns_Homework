import unittest
import json
import os
from general.deserializers.json_deserializer import JsonDeserializer
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomenclature import Nomenclature
from src.models.recipe import Recipe

class TestJsonDeserializer(unittest.TestCase):

    def setUp(self):
        self.deserializer = JsonDeserializer()
        self.output_dir = 'TestReportGeneration_folder\JSON'

    def test_deserialize_nomenclature_group_report_json(self):
        expected_group = NomenclatureGroup.default_group_source()
        json_file_path = os.path.join(self.output_dir, 'nomenclature_group_report.json')

        # Десериализуем данные из JSON-файла
        groups = self.deserializer.deserialize(json_file_path)

        # Проверяем, что десериализованные данные совпадают с ожидаемыми
        self.assertEqual(len(groups), 1) 
        self.assertEqual(groups[0].name, expected_group.name)

    def test_deserialize_measurement_unit_report_json(self):
        expected_unit = MeasurementUnit.default_unit_kg()
        json_file_path = os.path.join(self.output_dir, 'measurement_unit_report.json')

        # Десериализуем данные из JSON-файла
        units = self.deserializer.deserialize(json_file_path)

        # Проверяем, что десериализованные данные совпадают с ожидаемыми
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0].name, expected_unit.name)

    def test_deserialize_nomenclature_report_json(self):
        expected_nomenclature = Nomenclature()
        expected_nomenclature.name = "Тестовая Номенклатура"
        expected_nomenclature.group = NomenclatureGroup.default_group_source()
        expected_nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        json_file_path = os.path.join(self.output_dir, 'nomenclature_report.json')

        # Десериализуем данные из JSON-файла
        nomenclatures = self.deserializer.deserialize(json_file_path)

        # Проверяем, что десериализованные данные совпадают с ожидаемыми
        self.assertEqual(len(nomenclatures), 1)  # Ожидаем 1 номенклатуру
        self.assertEqual(nomenclatures[0].name, expected_nomenclature.name)
        self.assertEqual(nomenclatures[0].group.name, expected_nomenclature.group.name)
        self.assertEqual(nomenclatures[0].unit.name, expected_nomenclature.unit.name)

    def test_deserialize_recipe_report_json(self):
        expected_ingredients = [
            Nomenclature(name="Пшеничная мука", group=NomenclatureGroup.default_group_source(), unit=MeasurementUnit.default_unit_kg()),
            Nomenclature(name="Сахар", group=NomenclatureGroup.default_group_source(), unit=MeasurementUnit.default_unit_teaspoon())
        ]
        
        expected_recipe = Recipe()
        expected_recipe.name = "Тестовый Рецепт"
        expected_recipe.ingredients = expected_ingredients
        expected_recipe.steps = ["Шаг 1", "Шаг 2"]
        
        json_file_path = os.path.join(self.output_dir, 'recipe_report.json')

        # Десериализуем данные из JSON-файла
        recipes = self.deserializer.deserialize(json_file_path)

        # Проверяем, что десериализованные данные совпадают с ожидаемыми
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].name, expected_recipe.name)
        self.assertEqual(len(recipes[0].ingredients), len(expected_recipe.ingredients))
        self.assertEqual(recipes[0].steps, expected_recipe.steps)

    # def tearDown(self):
    #     self.clean_up()

    def clean_up(self):
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                os.remove(file_path)
            os.rmdir(self.output_dir)

if __name__ == '__main__':
    unittest.main()
