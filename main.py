from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse

import uvicorn

from api.models.server_models import *

from src.emuns.format_reporting import FormatReporting

from general.reports.report_factory import ReportFactory
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.domain_prototype import DomainPrototype
from general.filter.filter_dto import FilterDTO
from general.start_service import StartService
from general.data_reposity import DataReposity

from general.filter.filter_warehouse_nomenclature_dto import WarehouseNomenclatureFilterDTO
from general.prototypes.warehouse_transaction_prototype import WarehouseTransactionPrototype
from general.processors.process_factory import ProcessFactory
from general.processors.process_warehouse_turnover import WarehouseTurnoverProcess

from api.nomeclature_api import router as nomen_router


settings_manager = SettingsManager()
reposity = DataReposity()
recipe_manager = RecipeManager()
service = StartService(reposity, settings_manager, recipe_manager)
service.create()

app = FastAPI()

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
    
    reposity_data = reposity.data
    reposity_data_keys = reposity.keys
    
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
    
    reposity_data = reposity.data
    reposity_data_keys = reposity.keys
    
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

    data = reposity.data[reposity.warehouse_transaction_key()]
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
        
        data = reposity.data[DataReposity.warehouse_transaction_key()]
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)