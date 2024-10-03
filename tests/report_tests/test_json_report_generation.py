import unittest
import os
from general.reports.report_factory import ReportFactory
from src.emuns.format_reporting import FormatReporting
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomenclature import Nomenclature
from general.recipes.recipe import Recipe

class TestJSONReportGeneration(unittest.TestCase):

    def setUp(self):
        self.factory = ReportFactory()
        self.output_dir = 'TestReportGeneration_folder'

    def test_generate_nomenclature_group_report_json(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.JSON)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.json', FormatReporting.JSON)

    def test_generate_measurement_unit_report_json(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.JSON)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.json', FormatReporting.JSON)

    def test_generate_nomenclature_report_json(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.JSON)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.json', FormatReporting.JSON)

    def test_generate_recipe_report_json(self):
        ingredient1 = Nomenclature()
        ingredient1.name = "Пшеничная мука"
        ingredient1.group = NomenclatureGroup.default_group_source()
        ingredient1.unit = MeasurementUnit.default_unit_kg()

        ingredient2 = Nomenclature()
        ingredient2.name = "Сахар"
        ingredient2.group = NomenclatureGroup.default_group_source()
        ingredient2.unit = MeasurementUnit.default_unit_teaspoon()

        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = [ingredient1, ingredient2]
        recipe.steps = ["Шаг 1", "Шаг 2"]

        report = self.factory.create(FormatReporting.JSON)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.json', FormatReporting.JSON)

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
