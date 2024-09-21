import unittest
from unittest.mock import patch, mock_open
from general.recipes.recipe_manager import RecipeManager
from general.recipes.recipe import Recipe
from general.exception.exceptions import ArgumentException


class TestRecipeManager(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.manager = RecipeManager()

    @patch("builtins.open", new_callable=mock_open,
           read_data="""# Test Recipe
           
           | Ingredient | Amount |
           | ---------- | ------ |
           | Sugar sand | 100g   |
           | Egg        | 1 kg   |
           | Milk       | 500 ml |
           1. Mix ingredients
           2. Bake
           """)
    @patch("os.path.isfile", return_value=True)
    @patch("os.walk", return_value=[(".", [], ["recipe.md"])])
    def test_open_valid_file(self, mock_walk, mock_isfile, mock_open_file):
        """Тестирование успешного открытия файла рецепта."""
        result = self.manager.open("recipe.md")
        self.assertTrue(result)
        self.assertEqual(self.manager.recipe.name, "Test Recipe")
        self.assertEqual(self.manager.recipe.ingredients["Sugar sand"], "100g")
        self.assertEqual(self.manager.recipe.ingredients["Milk"], "500 ml")
        self.assertEqual(self.manager.recipe.steps, ["1. Mix ingredients", "2. Bake"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.isfile", return_value=False)
    def test_open_file_not_found(self, mock_isfile, mock_open_file):
        """Тестирование обработки отсутствующего файла рецепта."""
        result = self.manager.open("non_existent_file.md")
        self.assertFalse(result)
        self.assertEqual(self.manager.recipe.name, "РЕЦЕПТ НЕ БЫЛ НАЙДЕН")
        self.assertEqual(self.manager.recipe.ingredients["ИНГРИДИЕНТ 1"], "1")
        self.assertEqual(self.manager.recipe.steps, ["ШАГ 1", "ШАГ 2", "ШАГ 3"])

    @patch("os.walk", return_value=[(".", [], ["recipe.md"])])
    def test_get_file_path_file_not_found(self, mock_walk):
        """Тестирование поиска файла, когда файл не найден."""
        result = self.manager._get_file_path("non_existent_file.md")
        self.assertIsNone(result)

    def test_default_recipe(self):
        """Тестирование рецепта по умолчанию."""
        # default_recipe = self.manager._RecipeManager__default_recipe()
        default_recipe = self.manager._default_value()
        self.assertEqual(default_recipe.name, "РЕЦЕПТ НЕ БЫЛ НАЙДЕН")
        self.assertEqual(default_recipe.ingredients["ИНГРИДИЕНТ 1"], "1")
        self.assertEqual(default_recipe.steps, ["ШАГ 1", "ШАГ 2", "ШАГ 3"])

if __name__ == '__main__':
    unittest.main()
