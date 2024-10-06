import connexion
from flask import jsonify

from src.emuns.format_reporting import FormatReporting

from general.reports.report_factory import ReportFactory
from general.settings.settings_manager import SettingsManager
from general.recipes.recipe_manager import RecipeManager

from general.start_service import StartService
from general.data_reposity import DataReposity


app = connexion.FlaskApp(__name__)

@app.route("/report_formats", methods=["GET"])
def report_formats():
    return [{"name":item.name, "value": item.value} for item in FormatReporting]


@app.route("/report/<category>/<format_type>", methods=["GET"])
def create_report(category, format_type: str):
    settings_manager = SettingsManager()
    reposity = DataReposity()
    recipe_manager = RecipeManager()
    
    StartService(reposity, settings_manager, recipe_manager).create()
    
    data_reposity_keys = {
        'unit': reposity.unit_key(),
        'group': reposity.group_key(),
        'nomenclature': reposity.nomenclature_key(),
        'recipe': reposity.recipe_key()
    }
    
    if category not in data_reposity_keys:
        return jsonify({"Error": "Invalid category"}), 400
    try:
        report_format = FormatReporting[format_type.upper()]
    except KeyError:
        return jsonify({"Error": "Invalid report format"}), 400
    
    data = reposity.data[data_reposity_keys[category]]
    report = ReportFactory(settings_manager).create(report_format)
    report.create(data)
    
    return report.result, 200

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port = 8080)