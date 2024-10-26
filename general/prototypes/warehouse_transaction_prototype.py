from datetime import datetime

from src.models.warehouse_transaction import WarehouseTransaction
from general.filter.filter_dto import FilterDTO
from general.filter.filter_warehouse_nomenclature_dto import WarehouseNomenclatureFilterDTO

from general.domain_prototype import DomainPrototype
from general.exception.Validator_wrapper import ValidatorWrapper


class WarehouseTransactionPrototype(DomainPrototype):
    
    def create(self, data: list, filt: WarehouseNomenclatureFilterDTO):
        if filt.warehouse:
            self.data = self.filter_by_field(data, filt.warehouse, 'warehouse.name')

        if filt.nomenclature:
            self.data = self.filter_by_field(self.data, filt.nomenclature, 'nomenclature.name')

        if filt.start_period and filt.end_period:
            self.data = self.filter_by_period(self.data, filt.start_period, filt.end_period)

        return WarehouseTransactionPrototype(self.data)

    def filter_by_field(self, source: list, filt: FilterDTO, field: str):
        """
        Универсальная функция для фильтрации по указанному полю.
        """
        ValidatorWrapper.validate_not_none(source, 'source in WarehouseTransactionPrototype')
        ValidatorWrapper.validate_not_none(filt, 'filt in WarehouseTransactionPrototype')
        ValidatorWrapper.validate_non_empty(field, 'field in WarehouseTransactionPrototype')

        filter_value = getattr(filt, 'name', None)
        if not filter_value:
            return source

        result = []
        for item in source:
            item_field_value = self.extract_field(item, field)
            if self.match_field(item_field_value, filter_value, filt.type):
                result.append(item)

        return result

    def extract_field(self, item, field: str):
        fields = field.split('.')
        value = item
        for f in fields:
            value = getattr(value, f, None)
            if value is None:
                break
        return value

    def filter_by_period(self, source: list, start_period: datetime, end_period: datetime):
        ValidatorWrapper.validate_type(start_period, datetime, 'start_period in WarehouseTransactionPrototype')
        ValidatorWrapper.validate_type(end_period, datetime, 'start_period in WarehouseTransactionPrototype')

        result = []
        for item in source:
            if isinstance(item, WarehouseTransaction) and item.period:
                item_period = self.extract_field(item, 'period')
                if isinstance(item_period, str):
                    item_period = datetime.strptime(item_period, '%Y-%m-%d')

                if start_period <= item_period <= end_period:
                    result.append(item)

        return result