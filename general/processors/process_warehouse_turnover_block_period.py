from typing import List
from datetime import date

from src.models.warehouse_turnover import WarehouseTurnover
from src.models.warehouse_transaction import WarehouseTransaction

from src.emuns.transaction_types import TransactionTypes
from src.emuns.format_reporting import FormatReporting

from general.abstract_files.abstract_process import AbstractProcess
from general.exception.Validator_wrapper import ValidatorWrapper

from general.settings.settings_manager import SettingsManager

from general.reports.report_factory import ReportFactory

class BlockPeriodTurnoverProcessor(AbstractProcess):
    __start_period: date = date(year=1900, month=1, day=1)
    __setting_manager: SettingsManager = SettingsManager()
    
    def process(self, transactions: List[WarehouseTransaction]):
        block_period = self.__setting_manager.settings.block_period
        turnovers = {}

        for transaction in transactions:
            ValidatorWrapper.validate_type(transaction, WarehouseTransaction, "transactions in WarehouseTurnoverProcess")
            transaction_period = transaction.period.date()
            
            if transaction_period < self.__start_period or transaction_period > block_period:
                continue
            
            key = (transaction.warehouse.id, transaction.nomenclature.id, transaction.unit.id)
            
            if key not in turnovers:
                turnovers[key] = WarehouseTurnover(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    unit=transaction.unit
                )

            if transaction.transaction_type == TransactionTypes.INCOME:
                turnovers[key].flow += transaction.count
            else:
                turnovers[key].flow -= transaction.count

        return turnovers