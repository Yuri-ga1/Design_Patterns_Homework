from datetime import date
import os
import json

from general.abstract_files.abstract_logic import AbstractLogic
from general.filter.filter_dto import FilterDTO
from general.processors.process_warehouse_turnover_block_period import BlockPeriodTurnoverProcessor

from src.emuns.event_types import EventType

from general.domain_prototype import DomainPrototype
from general.services.observe_service import ObserverService

class TrialBalanceReport(AbstractLogic):
    
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        ObserverService.add(self)
    
    def create(self, params):
        data = params["transactions"]
        warehouse_filt = FilterDTO.create(params['warehouse_filter'].dict())
        
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, warehouse_filt)
        
        first_period, second_period = self.get_data_for_period(
            transaction=filtered_data.data,
            start_period=params['start_date'],
            end_period=params['end_date']
        )
        
        report_data = []
        all_keys = set(first_period.keys()).union(second_period.keys())
        
        for key in all_keys:
            nomenclature_name = first_period.get(key, second_period.get(key)).nomenclature.name
            unit_name = first_period.get(key, second_period.get(key)).unit.name
            
            
            flow_first = first_period[key].flow if key in first_period else 0
            flow_second = second_period[key].flow if key in second_period else 0
            total_flow = flow_first + flow_second
            
            report_data.append({
                "nomenclature_name": nomenclature_name,
                "unit": unit_name,
                "flow_first_period": flow_first,
                "flow_second_period": flow_second,
                "total_flow": total_flow
            })
        
        file_path = os.path.join('files', "trial_balance_report.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=4)
            
        return report_data
        
    
    def get_data_for_period(self, transaction, start_period: date, end_period: date = None):
        if not transaction:
            raise ValueError("No transactions found")
        
        blocked_process = BlockPeriodTurnoverProcessor()
        
        first_period = blocked_process.process(
                transactions=transaction,
                end_period=start_period
            )
        if not first_period:
            raise ValueError("No turnovers found for first period")
        
        second_period = blocked_process.process(
                transactions=transaction,
                start_period=start_period, 
                end_period=end_period
            )
        if not second_period:
            raise ValueError("No turnovers found for second period")
        
        return first_period, second_period
    
    def set_exception(self, ex):
        return super().set_exception(ex)
    
    def handle_event(self, type, params):
        super().handle_event(type, params)
        match type:
            case EventType.CREATE_TRIAL_BALANCE_REPORT:
                return self.create(params)
