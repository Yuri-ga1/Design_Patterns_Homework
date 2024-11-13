from typing import List

from src.models.warehouse_turnover import WarehouseTurnover
from src.models.warehouse_transaction import WarehouseTransaction

from src.emuns.transaction_types import TransactionTypes

from general.abstract_files.abstract_process import AbstractProcess
from general.exception.Validator_wrapper import ValidatorWrapper

class WarehouseTurnoverProcess(AbstractProcess):
    __blocked_turnovers: dict = {}
    
    def __init__(
        self,
        turnovers: dict = None,
    ):
        if turnovers:
            ValidatorWrapper.validate_type(turnovers, dict, "turnovers in BlockPeriodTurnoverProcessor __init__")
            self.__blocked_turnovers = turnovers
            
    def process(self, transactions: List[WarehouseTransaction]):
        turnovers = {}

        for transaction in transactions:
            ValidatorWrapper.validate_type(transaction, WarehouseTransaction, "transactions in WarehouseTurnoverProcess")
            
            key = (transaction.warehouse.id, transaction.nomenclature.id, transaction.unit.id)
            if key not in turnovers:
                turnovers[key] = WarehouseTurnover.create(
                    warehouse=transaction.warehouse,
                    nomenclature=transaction.nomenclature,
                    unit=transaction.unit
                )

            if transaction.transaction_type == TransactionTypes.INCOME:
                turnovers[key].flow += transaction.count
            else:
                turnovers[key].flow -= transaction.count
                
        for key, blocked_turnover in self.__blocked_turnovers.items():
            if key in turnovers:
                turnovers[key].flow += blocked_turnover.flow
            else:
                turnovers[key] = blocked_turnover

        return list(turnovers.values())