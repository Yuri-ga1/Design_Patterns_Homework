from general.exception.Validator_wrapper import ValidatorWrapper
from general.exception.exceptions import ArgumentException, OperationException

class Common:
    
    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        ValidatorWrapper.validate_type(source, object, 'source')  # Validate source type
        items = list(filter(lambda x: not x.startswith("_"), dir(source))) 
        result = []
        
        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                if is_common and (isinstance(value, dict) or isinstance(value, list)):
                    continue

                result.append(item)
                    
        return result
    
    @staticmethod
    def load_fields(data: dict, instance):
        ValidatorWrapper.validate_type(data, dict, 'data')  # Validate data type
        ValidatorWrapper.validate_type(instance, object, 'instance')  # Validate instance type

        fields = Common.get_fields(instance)

        for field in fields:
            keys = list(filter(lambda x: x == field, data.keys()))
            if len(keys) != 0:
                value = data[field]

                
                if not isinstance(value, (list, dict)):
                    setattr(instance, field, value)

        return instance            

    @staticmethod
    def load_list(data: list, instance, field: str, field_type):
        ValidatorWrapper.validate_type(data, list, "data")  # Validate data type
        ValidatorWrapper.validate_type(instance, object, 'instance')  # Validate instance type
        ValidatorWrapper.validate_type(field, str, 'field')  # Validate field type

        value = getattr(instance, field)
        if not isinstance(value, list):
            raise OperationException(f"Поле {field} не является списочным!")

        value.clear()

        for item in data:
            row = field_type()
            row = Common.load_fields(item, row)
            value.append(row)

        try:
            setattr(instance, field, value)
        except Exception as e:
            raise OperationException(f"Ошибка при добавлении списочного значения! {str(e)}")
