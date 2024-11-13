from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

import uvicorn

from api.models.server_models import *

from src.emuns.format_reporting import FormatReporting
from src.emuns.event_types import EventType

from general.reports.report_factory import ReportFactory
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.domain_prototype import DomainPrototype
from general.filter.filter_dto import FilterDTO
from general.data_reposity.data_reposity import DataReposity
from general.data_reposity.data_reposity_manager import DataReposityManager
from general.services.observe_service import ObserverService

from general.filter.filter_warehouse_nomenclature_dto import WarehouseNomenclatureFilterDTO
from general.prototypes.warehouse_transaction_prototype import WarehouseTransactionPrototype
from general.processors.process_warehouse_turnover_block_period import BlockPeriodTurnoverProcessor
from general.processors.process_factory import ProcessFactory
from general.processors.process_warehouse_turnover import WarehouseTurnoverProcess

from contextlib import asynccontextmanager

from api.nomeclature_api import router as nomen_router


settings_manager = SettingsManager()
recipe_manager = RecipeManager()

reposity_manager = DataReposityManager(
    recipe_manager=recipe_manager,
    settings_manager=settings_manager
)

observer_service = ObserverService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings_manager.settings.is_first_start:
        reposity_manager._default_value()
    else:
        reposity_manager.open(file_name=settings_manager.settings.data_source)
    yield
    observer_service.raise_event(EventType.SAVE_REPOSITY, params={"file_name": settings_manager.settings.data_source})

app = FastAPI(
    lifespan=lifespan
)

app.include_router(nomen_router)

# Маршрут для получения форматов отчетов
@app.get("/report_formats")
def report_formats():
    return [{"name": item.name, "value": item.value} for item in FormatReporting]

# Маршрут для создания отчета
@app.get("/report/{category}/{format_type}")
def create_report(form_data: CreateReportModel = Depends()):
    category = form_data.category
    format_type = form_data.format_type
    
    reposity_data = reposity_manager.reposity.data
    reposity_data_keys = reposity_manager.reposity.keys
    
    if category not in reposity_data_keys:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        report_format = FormatReporting[format_type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid report format")
    
    data = list(reposity_data[category])
    report = ReportFactory(settings_manager).create(report_format)
    report.create(data)
    
    return report.result


@app.post("/filter/{domain_type}")
async def filter_data(form_data: FilterDataModel = Depends()):
    domain_type = form_data.domain_type
    request = form_data.request
    
    reposity_data = reposity_manager.reposity.data
    reposity_data_keys = reposity_manager.reposity.keys
    
    if domain_type not in reposity_data_keys:
        raise HTTPException(status_code=400, detail="Invalid domain type")
    
    filter_data = await request.json()
    if not filter_data:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    try:
        filt = FilterDTO.create(filter_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    data = reposity_data[domain_type]
    if not data:
        raise HTTPException(status_code=404, detail="No data available")
    
    prototype = DomainPrototype(data)
    filtered_data = prototype.create(data, filt)
    
    if not filtered_data.data:
        raise HTTPException(status_code=404, detail="No data found")
    
    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)
    
    return report.result


@app.post("/transactions")
async def get_transactions(form_data: TransactionFilterRequest = Depends()):
    warehouse_filter = form_data.filter.warehouse
    nomenclature_filter = form_data.filter.nomenclature

    warehouse_filt = FilterDTO.create(warehouse_filter.dict())
    nomenclature_filt = FilterDTO.create(nomenclature_filter.dict())

    data = reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()]
    if not data:
        raise HTTPException(status_code=404, detail="No data available")

    prototype = DomainPrototype(data)
    filtered_data = prototype.create(data, warehouse_filt)
    filtered_data = prototype.create(filtered_data.data, nomenclature_filt)

    if not filtered_data.data:
        raise HTTPException(status_code=404, detail="No transactions found")

    # Создание отчета
    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)
    
    return report.result

@app.post("/turnover")
async def get_turnover(form_data: TurnoverFilterRequest = Depends()):
    try:
        warehouse_filt = WarehouseNomenclatureFilterDTO.create(form_data.filter.warehouse.dict())
        
        data = reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()]
        if not data:
            raise HTTPException(status_code=404, detail="No data available")

        prototype = WarehouseTransactionPrototype(data)
        filtered_data = prototype.create(data, warehouse_filt)

        if not filtered_data.data:
            raise HTTPException(status_code=404, detail="No transactions found")

        factory = ProcessFactory()
        factory.set_process('turnover', WarehouseTurnoverProcess)
        process = factory.get_process('turnover')
        turnovers = process.process(filtered_data.data)

        if not turnovers:
            raise HTTPException(status_code=404, detail="No turnovers found")

        report = ReportFactory(settings_manager).create(FormatReporting.JSON)
        report.create(turnovers)

        return JSONResponse(content=report.result)
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/update_block_period")
async def update_block_period(form_data: BlockPeriodForm = Depends()):
    try:
        block_period = form_data.block_period
        settings_manager.settings.block_period = block_period
        observer_service.raise_event(type=EventType.CHANGE_BLOCK_PERIOD, params=None)
        return {"message": "Block period successfully updated"}
    except:
        HTTPException(status_code=500, detail="Failed to update block period")

@app.get("/get_block_period")
async def get_block_period():
    return settings_manager.settings.block_period

@app.post("/save_reposity_data")
async def save_reposity_data(file_name: str):
    try:
        params ={
            "file_name": file_name,
        }
        statuses = observer_service.raise_event(EventType.SAVE_REPOSITY, params)
        return {"message": f"Reposity data was successfully saved {statuses}"}
    except Exception:
        HTTPException(status_code=500, detail="Failed to save save reposity data")
        
        
@app.post("/restore_reposity_data")
async def restore_reposity_data(file_name: str):
    try:
        params ={
            "file_name": file_name,
        }
        observer_service.raise_event(EventType.LOAD_REPOSITY, params)
        return {"data_reposity": reposity_manager.reposity.data}
    except Exception:
        HTTPException(status_code=500, detail="Failed to load reposity data")
        
@app.post("/get_trial_balance")
async def get_trial_balance(form_data: TrialBalanceForm = Depends()):
    try:
        warehouse_filter = form_data.warehouse
        warehouse_filt = FilterDTO.create(warehouse_filter.dict())
        
        start_date = form_data.start_date
        end_date= form_data.end_date
        
        data = reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()]
        if not data:
            raise HTTPException(status_code=404, detail="No data available")

        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, warehouse_filt)

        if not filtered_data:
            raise HTTPException(status_code=404, detail="No transactions found")
        
        blocked_process = BlockPeriodTurnoverProcessor()
        
        first_period = blocked_process.process(
                transactions=filtered_data.data,
                end_period=start_date
            )
        if not first_period:
            raise HTTPException(status_code=404, detail="No turnovers found for first period")
        
        second_period = blocked_process.process(
                transactions=filtered_data.data,
                start_period=start_date, 
                end_period=end_date
            )
        if not second_period:
            raise HTTPException(status_code=404, detail="No turnovers found for second period")


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

        return JSONResponse(content={
            "report": report_data,
        })
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)