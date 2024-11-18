import os
import random
from datetime import datetime, timedelta

from general.abstract_files.abstract_logic import AbstractLogic
from general.data_reposity.data_reposity import DataReposity
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from general.settings.settings_manager import SettingsManager
from general.settings.settings import Settings
from general.recipes.recipe_manager import RecipeManager

from src.models.Measurement_unit import MeasurementUnit
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.warehouse_transaction import WarehouseTransaction
from src.models.Warehouse import WarehouseModel

from src.emuns.transaction_types import TransactionTypes


"""
Сервис для реализации первого старта приложения
"""
class StartService(AbstractLogic):
    __reposity: DataReposity = None
    __settings_manager: SettingsManager = None
    __recipe_manager: RecipeManager = None

    def __init__(self, reposity: DataReposity, settings_manager: SettingsManager, recipe_manager: RecipeManager) -> None:
        super().__init__()
        Validator.validate_type(reposity, DataReposity, 'reposity')
        Validator.validate_type(settings_manager, SettingsManager, 'settings_manager')
        Validator.validate_type(recipe_manager, RecipeManager, 'recipe_manager')
        self.__reposity = reposity
        self.__settings_manager = settings_manager
        self.__recipe_manager = recipe_manager

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> Settings:
        return self.__settings_manager.settings

    def __create_nomenclature_groups(self):
        list = []
        list.append(NomenclatureGroup.default_group_cold())
        list.append( NomenclatureGroup.default_group_source())
        self.__reposity.data[self.__reposity.group_key()] = list

    def __create_nomenclature(self):
        directory = f'files{os.sep}recipes'
        ingredients = []
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            self.__recipe_manager.open(file_path)
            recipe_ing = self.__recipe_manager.recipe.ingredients
            ingredients.append(recipe_ing)
            
        
        flat_ingredients = [item for sublist in ingredients for item in sublist]
    
        unique_ingredients = list(set(flat_ingredients))

        self.__reposity.data[self.__reposity.nomenclature_key()] = unique_ingredients
            

    def __create_measurement_unit(self):
        kg_unit = MeasurementUnit.default_unit_kg()
        gramm_unit = MeasurementUnit.default_unit_gramm()
        thing_unit = MeasurementUnit.default_unit_thing()
        tablespoon_unit = MeasurementUnit.default_unit_tablespoon()
        teaspoon_unit = MeasurementUnit.default_unit_teaspoon()
        unit_list = [kg_unit, gramm_unit, thing_unit,
                     tablespoon_unit, teaspoon_unit]
        
        self.__reposity.data[self.__reposity.unit_key()] = unit_list
        
    def __create_receipts(self):
        recipe_files = ['waffles.md', 'chocolate_cookies.md']
        receipts_list = []
    
        for recipe_file in recipe_files:
            self.__recipe_manager.open(recipe_file)
            receipts_list.append(self.__recipe_manager.recipe)
    
        self.__reposity.data[self.__reposity.recipe_key()] = receipts_list
        
    def __create_warehouse(self):
        warehouse_list = []
        warehouse_list.append(WarehouseModel.create(
            name="Kolotushka",
            country="Russia",
            city="Irkutsk",
            street="Pushkina",
            house_number="6/A"
        ))
        
        warehouse_list.append(WarehouseModel.create(
            name="Pendos",
            country="America",
            city="New York",
            street="Ethnikis aminis",
            house_number="11"
        ))
        
        self.__reposity.data[self.__reposity.warehouse_key()] = warehouse_list
        
    def __create_warehouse_transaction(self):
        transactions = []
        nomenclatures = self.__reposity.data[self.__reposity.nomenclature_key()]
        units = self.__reposity.data[self.__reposity.unit_key()]
        warehouses = self.__reposity.data[self.__reposity.warehouse_key()]
        
        transaction_types = list(TransactionTypes)
        
        start_date = datetime(1900, 1, 1)
        end_date = datetime(2024, 10, 1)
        date_range_days = (end_date - start_date).days
    
        for _ in range(500):
            warehouse = random.choice(warehouses)
            
            nomenclature = random.choice(nomenclatures)
            unit = random.choice(units)

            count = random.uniform(0.1, 100.0)
            
            random_day = random.randint(0, date_range_days)
            period = start_date + timedelta(days=random_day)

            transaction = WarehouseTransaction.create(
                warehouse=warehouse,
                nomenclature=nomenclature,
                count=count,
                unit=unit,
                period=period,
                transaction_type=random.choice(transaction_types)
            )

            transactions.append(transaction)

        self.__reposity.data[self.__reposity.warehouse_transaction_key()] = transactions

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurement_unit()
        self.__create_nomenclature()
        self.__create_receipts()
        self.__create_warehouse()
        self.__create_warehouse_transaction()

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    

    def handle_event(self, type, params):
        return super().handle_event(type, params)

