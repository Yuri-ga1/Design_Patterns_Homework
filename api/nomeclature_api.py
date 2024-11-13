from fastapi import APIRouter, Query, Body

from general.services.nomenclature_service import NomenclatureService
from general.data_reposity.data_reposity import DataReposity
from general.reports.report_factory import ReportFactory
from general.settings.settings_manager import SettingsManager
from general.services.observe_service import ObserverService

from src.emuns.format_reporting import FormatReporting
from src.emuns.event_types import EventType

from api.models.pydantic_models import NomenclaturePydantic, NomenclatureWithUniqueCode

router = APIRouter(prefix='/nomenclature', tags=['Work with nomenclature'])

reposity=DataReposity()
settings_manager = SettingsManager()

nomenclature_service = NomenclatureService(reposity=reposity)


@router.get("/")
async def get_nomeclature(
        unique_code: str = Query(..., description="Nomenclature id")
    ):
    result = nomenclature_service.get(unique_code=unique_code)
    if result is None:
        return {"message": f"Nomenclature with id {unique_code} was not found"}
    
    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(result)
    
    return report.result

@router.post("/")
async def add_nomeclature(
    new_nomeclature: NomenclaturePydantic = Body(description="New nomenclature data")
):
    group_id = new_nomeclature.group.unique_code
    unit_id = new_nomeclature.unit.unique_code
    result = nomenclature_service.add(
        name=new_nomeclature.name,
        full_name=new_nomeclature.full_name,
        group_id=group_id,
        unit_id=unit_id,
    )
    return result

@router.delete("/")
async def delete_nomeclature(
    unique_code: str = Query(..., description="Nomenclature id")
):
    statuses = ObserverService.raise_event(type=EventType.DELETE_NOMENCLATURE, params=unique_code)
    return statuses[type(nomenclature_service).__name__]

@router.patch("/")
async def patch_nomeclature(
    update_nomeclature: NomenclatureWithUniqueCode = Body(description="Update nomenclature by id")
):
    params = {
        "unique_code": update_nomeclature.unique_code,
        "name": update_nomeclature.name,
        "full_name": update_nomeclature.full_name,
        "group_id": update_nomeclature.group_id,
        "unit_id": update_nomeclature.unit_id,
    }
    statuses = ObserverService.raise_event(type=EventType.CHANGE_NOMENCLATURE, params=params)
    return statuses[type(nomenclature_service).__name__]