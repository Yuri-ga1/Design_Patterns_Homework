from pydantic import BaseModel
from typing import Optional, Union
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


class UnitPydantic(BaseModel):
    unique_code: str
    name: str
    base_unit: Optional['UnitPydantic'] = None
    conversion_rate: Union[int, 'UnitPydantic']

class GroupPydantic(BaseModel):
    unique_code: str
    name: str


class NomenclaturePydantic(BaseModel):
    name: str
    full_name: str
    group: GroupPydantic
    unit: UnitPydantic 

class NomenclatureWithUniqueCode(BaseModel):
    unique_code: str
    name: Optional[str] = None
    full_name: Optional[str] = None
    group_id: Optional[str] = None
    unit_id: Optional[str] = None