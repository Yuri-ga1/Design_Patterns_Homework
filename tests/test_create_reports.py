import unittest
import os
from general.reports.report_factory import ReportFactory
from src.emuns.format_reporting import FormatReporting
from src.models.Nomeclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomeclature import Nomenclature
from general.recipes.recipe import Recipe

class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        self.factory = ReportFactory()
        self.output_dir = 'TestReportGeneration_folder'

    def test_generate_nomenclature_group_report_csv(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.CSV)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.csv', FormatReporting.CSV)

    def test_generate_nomenclature_group_report_json(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.JSON)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.json', FormatReporting.JSON)

    def test_generate_nomenclature_group_report_markdown(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.md', FormatReporting.MARKDOWN)

    def test_generate_nomenclature_group_report_rtf(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.RTF)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.rtf', FormatReporting.RTF)

    def test_generate_nomenclature_group_report_xml(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.XML)
        report.create([group])
        report.save_report(self.output_dir, 'nomenclature_group_report.xml', FormatReporting.XML)

    def test_generate_measurement_unit_report_csv(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.CSV)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.csv', FormatReporting.CSV)

    def test_generate_measurement_unit_report_json(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.JSON)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.json', FormatReporting.JSON)

    def test_generate_measurement_unit_report_markdown(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.md', FormatReporting.MARKDOWN)

    def test_generate_measurement_unit_report_rtf(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.RTF)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.rtf', FormatReporting.RTF)

    def test_generate_measurement_unit_report_xml(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.XML)
        report.create([unit])
        report.save_report(self.output_dir, 'measurement_unit_report.xml', FormatReporting.XML)

    def test_generate_nomenclature_report_csv(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.CSV)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.csv', FormatReporting.CSV)

    def test_generate_nomenclature_report_json(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.JSON)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.json', FormatReporting.JSON)

    def test_generate_nomenclature_report_markdown(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.md', FormatReporting.MARKDOWN)

    def test_generate_nomenclature_report_rtf(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.RTF)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.rtf', FormatReporting.RTF)

    def test_generate_nomenclature_report_xml(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.XML)
        report.create([nomenclature])
        report.save_report(self.output_dir, 'nomenclature_report.xml', FormatReporting.XML)

    def test_generate_recipe_report_csv(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.CSV)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.csv', FormatReporting.CSV)

    def test_generate_recipe_report_json(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.JSON)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.json', FormatReporting.JSON)

    def test_generate_recipe_report_markdown(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.md', FormatReporting.MARKDOWN)

    def test_generate_recipe_report_rtf(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.RTF)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.rtf', FormatReporting.RTF)

    def test_generate_recipe_report_xml(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.XML)
        report.create([recipe])
        report.save_report(self.output_dir, 'recipe_report.xml', FormatReporting.XML)

    # def tearDown(self):
    #     # Удаление сгенерированных файлов
    #     for folder in self.formats.values():
    #         folder_path = os.path.join(self.output_dir, folder)
    #         for filename in os.listdir(folder_path):
    #             file_path = os.path.join(folder_path, filename)
    #             os.remove(file_path)
    #         os.rmdir(folder_path)
    #     os.rmdir(self.output_dir)
