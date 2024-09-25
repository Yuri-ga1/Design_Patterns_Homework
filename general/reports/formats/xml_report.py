from src.emuns.format_reporting import FormatReporting
from general.abstract_files.abstract_report import AbstractReport
from general.exception.Validator_wrapper import ValidatorWrapper as Validator

from xml.etree.ElementTree import Element, SubElement, tostring

class XmlReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.XML
        
    
    def _object_to_xml(self, parent, obj):
        """
        Рекурсивно добавляет элементы объекта в XML. Если объект содержит вложенные объекты,
        они также добавляются как XML-элементы.
        """
        for field in dir(obj):
            if not field.startswith("_") and not callable(getattr(obj.__class__, field)):
                value = getattr(obj, field)

                if hasattr(value, '__dict__'):
                    sub_element = SubElement(parent, field)
                    self._object_to_xml(sub_element, value)
                elif isinstance(value, (list, tuple)):
                    for item in value:
                        sub_element = SubElement(parent, field)
                        if hasattr(item, '__dict__'):
                            self._object_to_xml(sub_element, item)
                        else:
                            sub_element.text = str(item)
                elif hasattr(value, 'name'):
                    sub_element = SubElement(parent, field)
                    sub_element.text = value.name
                else:
                    sub_element = SubElement(parent, field)
                    sub_element.text = str(value)
                    

    def create(self, data: list):
        Validator.validate_type(data, list, 'data')
        Validator.validate_not_empty_dataset(data)

        root = Element("root")

        for row in data:
            item = SubElement(root, "item")
            self._object_to_xml(item, row)

        self.result = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding='unicode')

