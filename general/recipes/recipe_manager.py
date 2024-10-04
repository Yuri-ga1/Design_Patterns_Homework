import re
from general.recipes.recipe import Recipe
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.abstract_files.abstract_manager import AbstractManager
from src.models.Nomenclature import Nomenclature
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit

class RecipeManager(AbstractManager):
    __file_name = ""
    __recipe: Recipe = None
    __nom_group: NomenclatureGroup = NomenclatureGroup()
    __meas_unit: MeasurementUnit = MeasurementUnit()

    def __init__(self) -> None:
        super().__init__()
        if self.__recipe is None:
            self.__recipe = self._default_value()

    def open(self, file_name: str = ""):
        Validator.validate_type(file_name, str, 'file_name')
        
        if file_name:
            self.__file_name = file_name

        try:
            full_name = self._get_file_path(self.__file_name)
            if full_name is None:
                self.__recipe = self._default_value()
                Validator.validate_file_exists(self.__file_name)
                
            with open(full_name, 'r', encoding="utf-8") as file:
                data = file.readlines()
                self.__parse_markdown(data)

            return True
        except Exception as e:
            print(f"Error reading file: {e}") 
            self.__recipe = self._default_value()
            return False

    @property
    def recipe(self):
        return self.__recipe

    def __parse_markdown(self, data: list):
        """Парсинг файла в формате markdown и заполнение объекта Recipe."""
        name = data[0].replace("# ", "").strip()
        ingredients = []
        steps = []
        header_and_row_counter = 0

        for line in data[1:]:
            line: str = line.strip()

            if line.startswith("####"):
                continue

            if line.startswith("|"):
                if header_and_row_counter < 2:
                    header_and_row_counter += 1
                    continue

                parts = line.split("|")
                ingredient_name = parts[1].strip()

                ingredient = Nomenclature()
                ingredient.name = ingredient_name
                ingredient.full_name = ingredient_name
                ingredient.group = self.__nom_group.default_group_source()
                ingredient.unit = self.__meas_unit.default_unit_gramm()
                ingredients.append(ingredient)

            elif re.match(r'^\d+', line) or line.startswith("-"):
                steps.append(line)

        self.__recipe.name = name
        self.__recipe.ingredients = ingredients
        self.__recipe.steps = steps

    def _default_value(self):
        """Задаем значения по умолчанию для рецепта."""
        data = Recipe()
        data.name = "РЕЦЕПТ НЕ БЫЛ НАЙДЕН"

        ingredient1 = Nomenclature()
        ingredient1.name = "ИНГРИДИЕНТ 1"
        ingredient1.full_name = "ИНГРИДИЕНТ 1"

        ingredient2 = Nomenclature()
        ingredient2.name = "ИНГРИДИЕНТ 2"
        ingredient2.full_name = "ИНГРИДИЕНТ 2"

        ingredient3 = Nomenclature()
        ingredient3.name = "ИНГРИДИЕНТ 3"
        ingredient3.full_name = "ИНГРИДИЕНТ 3"
        data.ingredients = [ingredient1, ingredient2, ingredient3]

        data.steps = [
            "ШАГ 1",
            "ШАГ 2",
            "ШАГ 3"
        ]
        return data
