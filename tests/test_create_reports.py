import unittest
import os
from src.models.Nomeclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomeclature import Nomenclature
from general.recipes.recipe import Recipe

class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        # Создание временной директории для отчетов
        self.report_dir = "test_created_files_for_1"
        os.makedirs(self.report_dir, exist_ok=True)

    def tearDown(self):
        # Удаление временной директории после тестов
        for file in os.listdir(self.report_dir):
            os.remove(os.path.join(self.report_dir, file))
        os.rmdir(self.report_dir)

    def test_generate_reports(self):
        # Создание объектов
        group = NomenclatureGroup.default_group_source()
        unit = MeasurementUnit.default_unit_kg()
        nomenclature = Nomenclature()
        nomenclature.name = "Тесто"
        nomenclature.full_name = "Тесто для пиццы"
        nomenclature.group = group
        nomenclature.unit = unit

        recipe = Recipe()
        recipe.name = "Пицца"
        recipe.ingredients = {
            nomenclature.name: 500  # 500 грамм теста
        }
        recipe.steps = ["Смешать ингредиенты", "Замесить тесто", "Выпекать 30 минут"]

        # Генерация отчетов
        with open(os.path.join(self.report_dir, 'nomenclature.txt'), 'w') as f:
            f.write(f"Название: {nomenclature.name}\n")
            f.write(f"Полное название: {nomenclature.full_name}\n")
            f.write(f"Группа: {group.name}\n")
            f.write(f"Единица измерения: {unit.name}\n")

        with open(os.path.join(self.report_dir, 'recipe.txt'), 'w') as f:
            f.write(f"Название рецепта: {recipe.name}\n")
            f.write("Ингредиенты:\n")
            for ingredient, amount in recipe.ingredients.items():
                f.write(f" - {ingredient}: {amount} грамм\n")
            f.write("Шаги:\n")
            for step in recipe.steps:
                f.write(f" - {step}\n")

        # Проверка, что файлы созданы
        self.assertTrue(os.path.exists(os.path.join(self.report_dir, 'nomenclature.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.report_dir, 'recipe.txt')))

if __name__ == "__main__":
    unittest.main()
