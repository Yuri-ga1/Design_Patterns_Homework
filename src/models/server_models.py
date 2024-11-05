from fastapi import Path, Query, Body
from datetime import date

from src.models.pydantic_models import *

class CreateReportModel:
    def __init__(
        self,
        category: str = Path(..., description="Data for the report (unit, group, nomenclature, recipes)"),
        format_type: str = Path(..., description="Report form (CSV, JSON, MARKDOWN, RTF, XML)"),
    ):
        self.category = category
        self.format_type = format_type

class FilterDataModel:
    def __init__(
        self,
        domain_type: str = Path(..., description="Model type for filter (unit, group, nomenclature, recipes)"),
        request: FilterDTOModel = Body(..., description="DTO model for filter"),
    ):
        self.domain_type = domain_type
        self.request = request
        
class TransactionFilterRequest:
    def __init__(self, filter: WarehouseNomenFilter = Body(...)):
        self.filter = filter
        
class TurnoverFilterRequest:
    def __init__(
        self,
        filter: WarehouseNomenFilter = Body(...),
        start_period: Optional[date] = Query(None, description="Period start (YYYY-MM-DD)"),
        end_period: Optional[date] = Query(None, description="Period end (YYYY-MM-DD)"),
    ):
        self.filter = filter
        self.start_period = start_period
        self.end_period = end_period
        
class BlockPeriodForm:
    def __init__(
        self,
        block_period: date = Query(None, description="Block period (YYYY-MM-DD)")
    ):
        self.block_period = block_period