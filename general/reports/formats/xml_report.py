from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from xml.etree.ElementTree import Element, SubElement, tostring

class XmlReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.XML

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        root = Element("root")

        for row in data:
            item = SubElement(root, "item")
            for field in dir(row):
                if not field.startswith("_") and not callable(getattr(row.__class__, field)):
                    field_element = SubElement(item, field)
                    field_element.text = str(getattr(row, field))

        self.result = tostring(root, encoding='unicode')
