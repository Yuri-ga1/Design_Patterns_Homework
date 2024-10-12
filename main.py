import connexion
from flask import jsonify, request

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

app = connexion.FlaskApp(__name__)

@app.route("/report_formats", methods=["GET"])
def report_formats():
    return [{"name":item.name, "value": item.value} for item in FormatReporting]


@app.route("/report/<category>/<format_type>", methods=["GET"])
def create_report(category, format_type: str):
    reposity_data = reposity.data
    reposity_data_keys = reposity.keys
    
    if category not in reposity_data_keys:
        return jsonify({"Error": "Invalid category"}), 400
    try:
        report_format = FormatReporting[format_type.upper()]
    except KeyError:
        return jsonify({"Error": "Invalid report format"}), 400
    
    data = list(reposity_data[category])
    report = ReportFactory(settings_manager).create(report_format)
    report.create(data)
    
    return report.result, 200

@app.route("/filter/<domain_type>", methods=["POST"])
def filter_data(domain_type):
    reposity_data = reposity.data
    reposity_data_keys = reposity.keys
    print("here7")

    if domain_type not in reposity_data_keys:
        return jsonify({"error": "Invalid domain type"}), 400
    print("here6")

    filter_data = request.get_json()
    if filter_data is None:
        return jsonify({"error": "Invalid JSON payload"}), 400
    print("here5")
    print(filter_data)

    try:
        filt = FilterDTO.from_dict(filter_data)
        print('filt = ', filt)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    print("here4")

    data = reposity_data[domain_type]
    if not data:
        return jsonify({"error": "No data available"}), 404
    print("here3")

    prototype = DomainPrototype(data)
    filtered_data = prototype.create(data, filt)

    if not filtered_data.data:
        return jsonify({"message": "No data found"}), 404
    print("here2")

    report = ReportFactory(settings_manager).create(FormatReporting.JSON)
    report.create(filtered_data.data)
    print("here1")
    return report.result, 200

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port = 8080)