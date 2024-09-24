import unittest
import os
from general.reports.report_factory import ReportFactory
from src.emuns.format_reporting import FormatReporting
from src.models.Nomeclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomeclature import Nomenclature
from general.recipes.recipe import Recipe
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        self.factory = ReportFactory()
        self.output_dir = 'TestReportGeneration_folder'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Создание подкаталогов для каждого типа файла
        self.formats = {
            FormatReporting.CSV: 'csv',
            FormatReporting.JSON: 'json',
            FormatReporting.MARKDOWN: 'markdown',
            FormatReporting.RTF: 'rtf',
            FormatReporting.XML: 'xml',
        }
        for folder in self.formats.values():
            os.makedirs(os.path.join(self.output_dir, folder), exist_ok=True)

    def save_report(self, report, report_name, format):
        folder_path = os.path.join(self.output_dir, self.formats[format])
        report_file_path = os.path.join(folder_path, report_name)
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(report.result)
        self.assertTrue(os.path.exists(report_file_path))

    def test_generate_nomenclature_group_report_csv(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.CSV)
        report.create([group])
        self.save_report(report, 'nomenclature_group_report.csv', FormatReporting.CSV)

    def test_generate_nomenclature_group_report_json(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.JSON)
        report.create([group])
        self.save_report(report, 'nomenclature_group_report.json', FormatReporting.JSON)

    def test_generate_nomenclature_group_report_markdown(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([group])
        self.save_report(report, 'nomenclature_group_report.md', FormatReporting.MARKDOWN)

    def test_generate_nomenclature_group_report_rtf(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.RTF)
        report.create([group])
        self.save_report(report, 'nomenclature_group_report.rtf', FormatReporting.RTF)

    def test_generate_nomenclature_group_report_xml(self):
        group = NomenclatureGroup.default_group_source()
        report = self.factory.create(FormatReporting.XML)
        report.create([group])
        self.save_report(report, 'nomenclature_group_report.xml', FormatReporting.XML)

    def test_generate_measurement_unit_report_csv(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.CSV)
        report.create([unit])
        self.save_report(report, 'measurement_unit_report.csv', FormatReporting.CSV)

    def test_generate_measurement_unit_report_json(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.JSON)
        report.create([unit])
        self.save_report(report, 'measurement_unit_report.json', FormatReporting.JSON)

    def test_generate_measurement_unit_report_markdown(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([unit])
        self.save_report(report, 'measurement_unit_report.md', FormatReporting.MARKDOWN)

    def test_generate_measurement_unit_report_rtf(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.RTF)
        report.create([unit])
        self.save_report(report, 'measurement_unit_report.rtf', FormatReporting.RTF)

    def test_generate_measurement_unit_report_xml(self):
        unit = MeasurementUnit.default_unit_kg()
        report = self.factory.create(FormatReporting.XML)
        report.create([unit])
        self.save_report(report, 'measurement_unit_report.xml', FormatReporting.XML)

    def test_generate_nomenclature_report_csv(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.CSV)
        report.create([nomenclature])
        self.save_report(report, 'nomenclature_report.csv', FormatReporting.CSV)

    def test_generate_nomenclature_report_json(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.JSON)
        report.create([nomenclature])
        self.save_report(report, 'nomenclature_report.json', FormatReporting.JSON)

    def test_generate_nomenclature_report_markdown(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([nomenclature])
        self.save_report(report, 'nomenclature_report.md', FormatReporting.MARKDOWN)

    def test_generate_nomenclature_report_rtf(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.RTF)
        report.create([nomenclature])
        self.save_report(report, 'nomenclature_report.rtf', FormatReporting.RTF)

    def test_generate_nomenclature_report_xml(self):
        nomenclature = Nomenclature()
        nomenclature.name = "Тестовая Номенклатура"
        nomenclature.group = NomenclatureGroup.default_group_source()
        nomenclature.unit = MeasurementUnit.default_unit_kg()
        
        report = self.factory.create(FormatReporting.XML)
        report.create([nomenclature])
        self.save_report(report, 'nomenclature_report.xml', FormatReporting.XML)

    def test_generate_recipe_report_csv(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.CSV)
        report.create([recipe])
        self.save_report(report, 'recipe_report.csv', FormatReporting.CSV)

    def test_generate_recipe_report_json(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.JSON)
        report.create([recipe])
        self.save_report(report, 'recipe_report.json', FormatReporting.JSON)

    def test_generate_recipe_report_markdown(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.MARKDOWN)
        report.create([recipe])
        self.save_report(report, 'recipe_report.md', FormatReporting.MARKDOWN)

    def test_generate_recipe_report_rtf(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.RTF)
        report.create([recipe])
        self.save_report(report, 'recipe_report.rtf', FormatReporting.RTF)

    def test_generate_recipe_report_xml(self):
        recipe = Recipe()
        recipe.name = "Тестовый Рецепт"
        recipe.ingredients = {"Ингредиент 1": 100, "Ингредиент 2": 200}
        recipe.steps = ["Шаг 1", "Шаг 2"]
        
        report = self.factory.create(FormatReporting.XML)
        report.create([recipe])
        self.save_report(report, 'recipe_report.xml', FormatReporting.XML)

    # def tearDown(self):
    #     # Удаление сгенерированных файлов
    #     for folder in self.formats.values():
    #         folder_path = os.path.join(self.output_dir, folder)
    #         for filename in os.listdir(folder_path):
    #             file_path = os.path.join(folder_path, filename)
    #             os.remove(file_path)
    #         os.rmdir(folder_path)
    #     os.rmdir(self.output_dir)
