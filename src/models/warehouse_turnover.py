from src.models.Warehouse import WarehouseModel
from src.models.Nomenclature import Nomenclature
from src.models.Measurement_unit import MeasurementUnit

from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper

class WarehouseTurnover(AbstractReference):
    __warehouse: WarehouseModel = WarehouseModel()
    __flow: float = 0.0
    __nomenclature: Nomenclature = Nomenclature()
    __unit: MeasurementUnit = MeasurementUnit()
    
    def __init__(
            self,
            warehouse: WarehouseModel = None,
            flow: float = 0.0,
            nomenclature: Nomenclature = None,
            unit: MeasurementUnit = None,
        ):
        if warehouse:
            ValidatorWrapper.validate_type(warehouse, WarehouseModel, "WarehouseModel")
            self.__warehouse = warehouse
        
        ValidatorWrapper.validate_type(flow, float, "flow")
        self.__flow = flow
        
        if nomenclature:
            ValidatorWrapper.validate_type(nomenclature, Nomenclature, "Nomenclature")
            self.__nomenclature = nomenclature
        
        if unit:
            ValidatorWrapper.validate_type(unit, MeasurementUnit, "MeasurementUnit")
            self.__unit = unit

    @property
    def warehouse(self):
        return self.__warehouse
    
    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        ValidatorWrapper.validate_type(value, WarehouseModel, "WarehouseModel setter")
        self.__warehouse = value

    @property
    def flow(self):
        return self.__flow
    
    @flow.setter
    def flow(self, value: float):
        ValidatorWrapper.validate_type(value, float, "flow")
        self.__flow = value

    @property
    def nomenclature(self):
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: Nomenclature):
        ValidatorWrapper.validate_type(value, Nomenclature, "Nomenclature")
        self.__nomenclature = value

    @property
    def unit(self):
        return self.__unit
    
    @unit.setter
    def unit(self, value: MeasurementUnit):
        ValidatorWrapper.validate_type(value, MeasurementUnit, "MeasurementUnit")
        self.__unit = value

    def __eq__(self, other):
        if isinstance(other, WarehouseTurnover):
            return (self.warehouse == other.warehouse and
                    self.flow == other.flow and
                    self.nomenclature == other.nomenclature and
                    self.unit == other.unit)
        return NotImplemented
