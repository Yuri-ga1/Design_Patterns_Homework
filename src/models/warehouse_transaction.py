from datetime import datetime

from src.models.Warehouse import WarehouseModel
from src.models.Nomenclature import Nomenclature
from src.models.Measurement_unit import MeasurementUnit

from src.emuns.transaction_types import TransactionTypes

from general.abstract_files.abstract_model import AbstractReference
from general.exception.Validator_wrapper import ValidatorWrapper

class WarehouseTransaction(AbstractReference):
    __warehouse: WarehouseModel = WarehouseModel()
    __nomenclature: Nomenclature = Nomenclature()
    __count: float = 0.0
    __unit: MeasurementUnit = MeasurementUnit()
    __period: datetime = datetime.now()
    __transaction_type: TransactionTypes = TransactionTypes.INCOME
    
    @staticmethod
    def create(
        warehouse: WarehouseModel,
        nomenclature: Nomenclature,
        unit: MeasurementUnit,
        count: float = 0.0,
        period: datetime = datetime.now(),
        transaction_type: TransactionTypes = TransactionTypes.INCOME,
    ):
        transaction = WarehouseTransaction()
        transaction.warehouse = warehouse
        transaction.nomenclature = nomenclature
        transaction.unit = unit
        transaction.count = count
        transaction.period = period
        transaction.transaction_type = transaction_type
        return transaction

    @property
    def warehouse(self):
        return self.__warehouse
    
    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        ValidatorWrapper.validate_type(value, WarehouseModel, "WarehouseModel setter")
        self.__warehouse = value

    @property
    def nomenclature(self):
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value):
        ValidatorWrapper.validate_type(value, Nomenclature, "Nomenclature")
        self.__nomenclature = value

    @property
    def count(self):
        return self.__count
    
    @count.setter
    def count(self, value):
        ValidatorWrapper.validate_type(value, float, "count")
        self.__count = value

    @property
    def unit(self):
        return self.__unit
    
    @unit.setter
    def unit(self, value):
        ValidatorWrapper.validate_type(value, MeasurementUnit, "MeasurementUnit")
        self.__unit = value

    @property
    def period(self):
        return self.__period
    
    @period.setter
    def period(self, value):
        ValidatorWrapper.validate_type(value, datetime, "period")
        self.__period = value
        
    @property
    def transaction_type(self):
        return self.__transaction_type
    
    @transaction_type.setter
    def transaction_type(self, value):
        ValidatorWrapper.validate_type(value, TransactionTypes, "transaction_type setter")
        self.__transaction_type = value

    def __eq__(self, other):
        if isinstance(other, WarehouseTransaction):
            return (self.warehouse == other.warehouse and
                    self.nomenclature == other.nomenclature and
                    self.count == other.count and
                    self.unit == other.unit and
                    self.transaction_type == other.transaction_type and
                    self.period == other.period)
        return NotImplemented
