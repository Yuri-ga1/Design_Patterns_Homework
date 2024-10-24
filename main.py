from fastapi import FastAPI, HTTPException, Request, Depends

import uvicorn

from src.models.server_models import *

from src.emuns.format_reporting import FormatReporting

from general.reports.report_factory import ReportFactory
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager
from general.domain_prototype import DomainPrototype
from general.filter.filter_dto import FilterDTO
from general.start_service import StartService
from general.data_reposity import DataReposity


settings_manager = SettingsManager()
reposity = DataReposity()
recipe_manager = RecipeManager()
service = StartService(reposity, settings_manager, recipe_manager)
service.create()

app = FastAPI()

# Маршрут для получения форматов отчетов
@app.get("/report_formats")
def report_formats():
    return [{"name": item.name, "value": item.value} for item in FormatReporting]

# Маршрут для создания отчета
@app.get("/report/{category}/{format_type}")
def create_report(form_data: CreateReportModel = Depends()):
    reposity_data = reposity.data
    reposity_data_keys = reposity.keys
    
    category = form_data.category
    format_type = form_data.format_type
    
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
        filt = FilterDTO.from_json(filter_data)
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)