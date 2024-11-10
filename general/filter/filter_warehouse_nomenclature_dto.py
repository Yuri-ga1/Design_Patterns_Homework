from datetime import datetime

from general.filter.filter_dto import FilterDTO

from general.exception.Validator_wrapper import ValidatorWrapper as Validator
from general.abstract_files.abstract_logic import AbstractLogic
from general.exception.exceptions import ArgumentException

class WarehouseNomenclatureFilterDTO(AbstractLogic):
    __warehouse: FilterDTO = None
    __nomenclature: FilterDTO = None
    __start_period: datetime = None
    __end_period: datetime = None
    
    def __init__(self, warehouse: FilterDTO = None, nomenclature: FilterDTO = None, start_period: datetime = None, end_period: datetime = None):
        if warehouse:
            Validator.validate_type(warehouse, FilterDTO, "warehouse in WarehouseNomenclatureFilterDTO")
            self.__warehouse = warehouse
            
        if nomenclature:
            Validator.validate_type(nomenclature, FilterDTO, "nomenclature in WarehouseNomenclatureFilterDTO")
            self.__nomenclature = nomenclature
            
        if start_period:
            Validator.validate_type(start_period, datetime, "start_period in WarehouseNomenclatureFilterDTO")
            self.__start_period = start_period
            
        if start_period:
            Validator.validate_type(end_period, datetime, "end_period in WarehouseNomenclatureFilterDTO")
            self.__end_period = end_period

    @property
    def warehouse(self):
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: FilterDTO):
        Validator.validate_type(value, FilterDTO, "value in WarehouseNomenclatureFilterDTO")
        self.__warehouse = value

    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: FilterDTO):
        Validator.validate_type(value, FilterDTO, "value in WarehouseNomenclatureFilterDTO")
        self.__nomenclature = value

    @property
    def start_period(self):
        return self.__start_period

    @start_period.setter
    def start_period(self, value: datetime):
        Validator.validate_type(value, datetime, "value in WarehouseNomenclatureFilterDTO")
        self.__start_period = value
        
    @property
    def end_period(self):
        return self.__end_period

    @end_period.setter
    def end_period(self, value: datetime):
        Validator.validate_type(value, datetime, "value in WarehouseNomenclatureFilterDTO")
        self.__end_period = value
        

    @staticmethod
    def create(data: dict):
        Validator.validate_type(data, dict, "data in WarehouseNomenclatureFilterDTO")
        try:
            warehouse_data = data.get('warehouse', {})
            nomenclature_data = data.get('nomenclature', {})
            start_period = data.get('start_period', None)
            end_period = data.get('end_period', None)

            warehouse = FilterDTO.create(warehouse_data)
            nomenclature = FilterDTO.create(nomenclature_data)

            return WarehouseNomenclatureFilterDTO(
                warehouse=warehouse,
                nomenclature=nomenclature,
                start_period=start_period,
                end_period=end_period
            )
        except ArgumentException as ex:
            WarehouseNomenclatureFilterDTO().set_exception(ex)
        except Exception as ex:
            WarehouseNomenclatureFilterDTO().set_exception(ex)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
        
    def handle_event(self, type, params):
        return super().handle_event(type, params)
        