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
    __turnovers: dict = {}
    __start_period: date = date(year=1900, month=1, day=1)
    __setting_manager: SettingsManager = SettingsManager()
    __factory: ReportFactory = ReportFactory()
    
    def process(self, transactions: List[WarehouseTransaction]):
        block_period = self.__setting_manager.settings.block_period
        self.__turnovers = {}

        for transaction in transactions:
            ValidatorWrapper.validate_type(transaction, WarehouseTransaction, "transactions in WarehouseTurnoverProcess")
            
            if transaction.period < self.__start_period and transaction.period > block_period:
                continue
            
            key = (transaction.warehouse.id, transaction.nomenclature.id, transaction.unit.id)
            if key not in self.__turnovers:
                self.__turnovers[key] = WarehouseTurnover(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    unit=transaction.unit
                )

            if transaction.transaction_type == TransactionTypes.INCOME:
                self.__turnovers[key].flow += transaction.count
            else:
                self.__turnovers[key].flow -= transaction.count

        return list(self.__turnovers.values())
    
    def save(self, filename):
        report = self.__factory.create(FormatReporting.JSON)
        report.create(list(self.__turnovers.values()))
        report.save_report("turnover_block_period", f'{filename}.json', FormatReporting.JSON)