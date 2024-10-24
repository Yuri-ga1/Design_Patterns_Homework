from fastapi import Path, Query, Body
from fastapi import Request

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