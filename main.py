from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
import os
import traceback

import uvicorn

from api.models.server_models import *

from src.emuns.format_reporting import FormatReporting
from src.emuns.event_types import EventType

from general.logger import Logger
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
from general.reports.trial_balance import TrialBalanceReport
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

trial_balance_report = TrialBalanceReport(settings_manager=settings_manager)

logger = Logger(
    log_file=settings_manager.settings.log_filename,
    file_level=settings_manager.settings.file_log_level,
    console_level=settings_manager.settings.console_log_level,
    enable_console=settings_manager.settings.enable_console,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    if settings_manager.settings.is_first_start:
        reposity_manager._default_value()
        logger.debug("First start, initialized default values.")
    else:
        reposity_manager.open(file_name=settings_manager.settings.data_source)
        logger.debug(f"Opened data source: {settings_manager.settings.data_source}")
    yield
    observer_service.raise_event(EventType.SAVE_SETTINGS, params=None)
    observer_service.raise_event(EventType.SAVE_REPOSITY, params={"file_name": settings_manager.settings.data_source})

app = FastAPI(
    lifespan=lifespan
)

app.include_router(nomen_router)

# Маршрут для получения форматов отчетов
@app.get("/report_formats")
def report_formats():
    logger.debug("User getting report formats")
    return [{"name": item.name, "value": item.value} for item in FormatReporting]

# Маршрут для создания отчета
@app.get("/report/{category}/{format_type}")
def create_report(form_data: CreateReportModel = Depends()):
    logger.info(f"Creating report for category: {form_data.category}, format: {form_data.format_type}")
    category = form_data.category
    format_type = form_data.format_type
    
    reposity_data = reposity_manager.reposity.data
    reposity_data_keys = reposity_manager.reposity.keys
    
    if category not in reposity_data_keys:
        logger.error(f"Invalid category: {category}")
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        report_format = FormatReporting[format_type.upper()]
    except KeyError:
        logger.error(f"Invalid report format: {format_type}")
        raise HTTPException(status_code=400, detail="Invalid report format")
    
    data = list(reposity_data[category])
    report = ReportFactory(settings_manager).create(report_format)
    report.create(data)
    
    logger.info(f"Report created successfully with {len(data)} records.")
    return report.result


@app.post("/filter/{domain_type}")
async def filter_data(form_data: FilterDataModel = Depends()):
    logger.info(f"Filtering data for domain type: {form_data.domain_type}")
    domain_type = form_data.domain_type
    request = form_data.request
    
    reposity_data = reposity_manager.reposity.data
    reposity_data_keys = reposity_manager.reposity.keys
    
    if domain_type not in reposity_data_keys:
        logger.error(f"Invalid domain type: {domain_type}")
        raise HTTPException(status_code=400, detail="Invalid domain type")
    
    filter_data = await request.json()
    if not filter_data:
        logger.error("Invalid JSON payload")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    try:
        filt = FilterDTO.create(filter_data)
    except Exception as e:
        logger.error(f"Error in filter data:\n {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    
    data = reposity_data[domain_type]
    if not data:
        logger.error(f"No data available for domain type: {domain_type}")
        raise HTTPException(status_code=404, detail="No data available")
    
    prototype = DomainPrototype(data)
    filtered_data = prototype.create(data, filt)
    
    if not filtered_data.data:
        logger.error(f"No data found after filtering domain type: {domain_type}")
        raise HTTPException(status_code=404, detail="No data found")
    
    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)
    
    logger.info(f"Filtered data for domain type {domain_type} successfully")
    return report.result


@app.post("/transactions")
async def get_transactions(form_data: TransactionFilterRequest = Depends()):
    logger.info(f"Filtering transactions with warehouse: {form_data.filter.warehouse} and nomenclature: {form_data.filter.nomenclature}")
    warehouse_filter = form_data.filter.warehouse
    nomenclature_filter = form_data.filter.nomenclature

    warehouse_filt = FilterDTO.create(warehouse_filter.dict())
    nomenclature_filt = FilterDTO.create(nomenclature_filter.dict())

    data = reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()]
    if not data:
        logger.error("No data available for warehouse transactions")
        raise HTTPException(status_code=404, detail="No data available")

    prototype = DomainPrototype(data)
    filtered_data = prototype.create(data, warehouse_filt)
    filtered_data = prototype.create(filtered_data.data, nomenclature_filt)

    if not filtered_data.data:
        logger.error("No transactions found after filtering")
        raise HTTPException(status_code=404, detail="No transactions found")

    # Создание отчета
    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)
    
    logger.info("Transactions filtered and report created successfully")
    return report.result

@app.post("/turnover")
async def get_turnover(form_data: TurnoverFilterRequest = Depends()):
    try:
        logger.info(f"Calculating turnover with warehouse filter: {form_data.filter.warehouse}")

        warehouse_filt = WarehouseNomenclatureFilterDTO.create(form_data.filter.warehouse.dict())
        
        data = reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()]
        if not data:
            logger.error("No data available for warehouse transactions")
            raise HTTPException(status_code=404, detail="No data available")

        prototype = WarehouseTransactionPrototype(data)
        filtered_data = prototype.create(data, warehouse_filt)

        if not filtered_data.data:
            logger.error("No transactions found after filtering")
            raise HTTPException(status_code=404, detail="No transactions found")

        factory = ProcessFactory()
        factory.set_process('turnover', WarehouseTurnoverProcess)
        process = factory.get_process('turnover')
        turnovers = process.process(filtered_data.data)

        if not turnovers:
            logger.error("No turnovers found")
            raise HTTPException(status_code=404, detail="No turnovers found")

        report = ReportFactory(settings_manager).create(FormatReporting.JSON)
        report.create(turnovers)

        logger.info("Turnover processed and report created successfully")
        return JSONResponse(content=report.result)
        
    except Exception as e:
        logger.error(f"Error during turnover processing:\n {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/update_block_period")
async def update_block_period(form_data: BlockPeriodForm = Depends()):
    try:
        logger.info(f"Updating block period to {form_data.block_period}")
        block_period = form_data.block_period
        settings_manager.settings.block_period = block_period
        observer_service.raise_event(type=EventType.CHANGE_BLOCK_PERIOD, params=None)
        return {"message": "Block period successfully updated"}
    except Exception as e:
        logger.error(f"Failed to update block period:\n {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to update block period")

@app.get("/get_block_period")
async def get_block_period():
    logger.info("Retrieving current block period")
    return settings_manager.settings.block_period

@app.post("/save_reposity_data")
async def save_reposity_data(file_name: str):
    try:
        logger.info(f"Saving repository data to file: {file_name}")
        params = {
            "file_name": file_name,
        }
        statuses = observer_service.raise_event(EventType.SAVE_REPOSITY, params)
        return {"message": f"Reposity data was successfully saved {statuses}"}
    except Exception as e:
        logger.error(f"Failed to save repository data:\n {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to save reposity data")

@app.post("/restore_reposity_data")
async def restore_reposity_data(file_name: str):
    try:
        logger.info(f"Restoring repository data from file: {file_name}")
        params = {
            "file_name": file_name,
        }
        observer_service.raise_event(EventType.LOAD_REPOSITY, params)
        return {"data_reposity": reposity_manager.reposity.data}
    except Exception as e:
        logger.error(f"Failed to load repository data:\n {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to load reposity data")

@app.post("/create_trial_balance")
async def create_trial_balance(form_data: TrialBalanceForm = Depends()):
    try:
        logger.info(f"Creating trial balance report for warehouse: {form_data.warehouse}")
        
        params = {
            'transactions': reposity_manager.reposity.data[DataReposity.warehouse_transaction_key()],
            'warehouse_filter': form_data.warehouse,
            'start_date': form_data.start_date,
            'end_date': form_data.end_date
        }
        
        observer_service.raise_event(EventType.CREATE_TRIAL_BALANCE_REPORT, params)
        
        file_path = os.path.join('files', "trial_balance_report.json")
        with open(file_path, "r", encoding="utf-8") as json_file:
            result = json.load(json_file)
            
        logger.info("Trial balance report created successfully")
        return result
    
    except Exception as e:
        logger.error(f"Error during trial balance report creation:\n {traceback.format_exc()}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
