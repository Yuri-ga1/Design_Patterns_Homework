from pydantic import BaseModel
from typing import Optional
from src.emuns.filter_types import FilterTypes

from src.models.Nomenclature import Nomenclature
from src.models.Nomenclature_group import NomenclatureGroup
from src.models.Measurement_unit import MeasurementUnit

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


class NomenclaturePydantic(BaseModel):
    name: str
    full_name: str
    group_id: str
    unit_id: str
    
class NomenclatureWithUniqueCode(BaseModel):
    unique_code: str
    name: Optional[str] = None
    full_name: Optional[str] = None
    group_id: Optional[str] = None
    unit_id: Optional[str] = None