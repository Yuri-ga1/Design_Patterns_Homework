from pydantic import BaseModel
from typing import Optional
from src.emuns.filter_types import FilterTypes

class FilterDTOModel(BaseModel):
    name: str | None = None
    unique_code: str | None = None
    type: str | None = None
    
class OptionalFilterDTOModel(BaseModel):
    name: Optional[str] = ""
    unique_code: Optional[str] = ""
    type: Optional[str] = FilterTypes.LIKE

class WarehouseNomenFilter(BaseModel):
    warehouse: Optional[OptionalFilterDTOModel] = None
    nomenclature: Optional[OptionalFilterDTOModel] = None