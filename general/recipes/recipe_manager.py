import re
from .recipe import Recipe
from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.abstract_files.abstract_manager import AbstractManager

class RecipeManager(AbstractManager):
    __file_name = ""
    __recipe: Recipe = None

    def __init__(self) -> None:
        super().__init__()
        if self.__recipe is None:
            self._default_value()

    def open(self, file_name: str = ""):
        Validator.validate_type(file_name, str, 'file_name')
        
        if file_name != "":
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
        except:
            self.__recipe = self._default_value()
            return False

    @property
    def recipe(self):
        return self.__recipe

    def __parse_markdown(self, data: list):
        name = data[0].replace("# ", "").strip()
        ingredients = {}
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
                amount = parts[2].strip()
                ingredients[ingredient_name] = amount

            elif re.match(r'^\d+', line) or line.startswith("-"):
                steps.append(line)

        self.__recipe.name = name
        self.__recipe.ingredients = ingredients
        self.__recipe.steps = steps

    def _default_value(self):
        data = Recipe()
        data.name = "РЕЦЕПТ НЕ БЫЛ НАЙДЕН"
        data.ingredients = {
            "ИНГРИДИЕНТ 1": "1",
            "ИНГРИДИЕНТ 2": "2",
            "ИНГРИДИЕНТ 3": "3",
        }
        data.steps = [
            "ШАГ 1",
            "ШАГ 2",
            "ШАГ 3"
        ]
        return data
