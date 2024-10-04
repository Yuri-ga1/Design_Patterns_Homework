import unittest
from unittest.mock import patch, mock_open
from general.recipes.recipe_manager import RecipeManager
from general.recipes.recipe import Recipe
from src.models.Nomenclature import Nomenclature

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
        result = self.manager.open("waffles.md")
        self.assertTrue(result)
        self.assertEqual(self.manager.recipe.name, "Test Recipe")
        
        print('\n', self.manager.recipe.ingredients)
        
        self.assertEqual(len(self.manager.recipe.ingredients), 3)

        # Проверка конкретных ингредиентов
        ingredient_names = [ingredient.name for ingredient in self.manager.recipe.ingredients]
        self.assertIn("Sugar sand", ingredient_names)
        self.assertIn("Egg", ingredient_names)
        self.assertIn("Milk", ingredient_names)

        # Проверяем шаги
        self.assertEqual(self.manager.recipe.steps, ["1. Mix ingredients", "2. Bake"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.isfile", return_value=False)
    def test_open_file_not_found(self, mock_isfile, mock_open_file):
        """Тестирование обработки отсутствующего файла рецепта."""
        result = self.manager.open("non_existent_file.md")
        self.assertFalse(result)
        self.assertEqual(self.manager.recipe.name, "РЕЦЕПТ НЕ БЫЛ НАЙДЕН")
        self.assertEqual(len(self.manager.recipe.ingredients), 3)  # Убедитесь, что есть три ингредиента по умолчанию
        self.assertEqual(self.manager.recipe.ingredients[0].name, "ИНГРИДИЕНТ 1")
        self.assertEqual(self.manager.recipe.ingredients[1].name, "ИНГРИДИЕНТ 2")
        self.assertEqual(self.manager.recipe.ingredients[2].name, "ИНГРИДИЕНТ 3")
        self.assertEqual(self.manager.recipe.steps, ["ШАГ 1", "ШАГ 2", "ШАГ 3"])

    @patch("os.walk", return_value=[(".", [], ["recipe.md"])])
    def test_get_file_path_file_not_found(self, mock_walk):
        """Тестирование поиска файла, когда файл не найден."""
        result = self.manager._get_file_path("non_existent_file.md")
        self.assertIsNone(result)

    def test_default_recipe(self):
        """Тестирование рецепта по умолчанию."""
        default_recipe = self.manager._default_value()
        self.assertEqual(default_recipe.name, "РЕЦЕПТ НЕ БЫЛ НАЙДЕН")
        self.assertEqual(len(default_recipe.ingredients), 3)  # Убедитесь, что есть три ингредиента
        self.assertEqual(default_recipe.ingredients[0].name, "ИНГРИДИЕНТ 1")
        self.assertEqual(default_recipe.ingredients[1].name, "ИНГРИДИЕНТ 2")
        self.assertEqual(default_recipe.ingredients[2].name, "ИНГРИДИЕНТ 3")
        self.assertEqual(default_recipe.steps, ["ШАГ 1", "ШАГ 2", "ШАГ 3"])


if __name__ == '__main__':
    unittest.main()
