from general.data_reposity import DataReposity
from general.abstract_files.abstract_logic import AbstractLogic
from general.exception.Validator_wrapper import ValidatorWrapper
from general.filter.filter_dto import FilterDTO

from general.domain_prototype import DomainPrototype
from src.models.Nomenclature import Nomenclature

from src.emuns.filter_types import FilterTypes
from src.emuns.event_types import EventType


class NomenclatureService(AbstractLogic):
    
    def __init__(self, reposity: DataReposity):
        ValidatorWrapper.validate_type(reposity, DataReposity, "reposity in NomenclatureService __init__")
        self.reposity = reposity
    
    def add(self, name, full_name, group_id, unit_id):
        try:
            group = self.get_group_by_id(group_id)
            if group is None:
                return {"message": f"Group with id {group_id} is not exist"}
            
            unit = self.get_unit_by_id(unit_id)
            if unit is None:
                return {"message": f"Unit with id {unit_id} is not exist"}

            new_nomeclature = Nomenclature.create(
                name=name,
                full_name=full_name,
                group=group,
                unit=unit,
            )
            self.reposity[DataReposity.nomenclature_key()].append(new_nomeclature)
            return {"message": "New nomenclature add successfully"}
        except Exception as e:
            return {"message": "Something went wrong while add new nomenclature"}
    
    def get(self, unique_code: str):
        ValidatorWrapper.validate_type(unique_code, str, "unique_code in NomenclatureService get function")
        filter = FilterDTO(
            unique_code=unique_code,
            type_value=FilterTypes.EQUALS
        )
        
        filtered = next(
                iter(
                    self.filter_data(
                        filt=filter
                    )
                )
                , None
            )
        return filtered
    
    def update(self, params):
        unique_code = params["unique_code"]
        
        nomenclature = self.get(unique_code=unique_code)
        
        if nomenclature is None:
            return {"message": f"Nomenclature with id {unique_code} is not exist"}
        
        self.update_nomenclature(
            nomenclature=nomenclature,
            params=params
        )
            
        self.update_nomenclature_in_recipes(unique_code, params)
        self.update_nomenclature_in_transactions(unique_code, params)
        
        return {"message": f"Nomenclature with id {unique_code} updated successfully"}
             
        
    def delete(self, unique_code: str):
        nomenclature = self.get(unique_code=unique_code)
        
        if nomenclature is None:
            return {"message": f"Nomenclature with id {unique_code} is not exist"}
        
        if self.is_in_recipes(unique_code) and self.is_in_transaction(unique_code):
            return {"message": f"Nomenclature with id {unique_code} used in recipes or in transactions"}
        
        self.reposity[DataReposity.nomenclature_key()] = [
            nom for nom in self.reposity[DataReposity.nomenclature_key()] if nom.id != unique_code
        ]
        
        return {"message": f"Nomenclature with id {unique_code} successfully deleted"}
    
    
    def filter_data(self, filt: FilterDTO, key=DataReposity.nomenclature_key()):
        data = self.reposity.data.get(key, [])
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, filt)
        return filtered_data.data
    
    def is_in_recipes(self, nomenclature_id: str):
        filter = FilterDTO(unique_code=nomenclature_id)
        filtered = self.filter_data(filt=filter, key=DataReposity.recipe_key())
        return len(filtered) > 0
    
    def is_in_transaction(self, nomenclature_id: str):
        filter = FilterDTO(unique_code=nomenclature_id)
        filtered = self.filter_data(filt=filter, key=DataReposity.warehouse_transaction_key())
        return len(filtered) > 0 
    
    def get_group_by_id(self, group_id):
        group_filter = FilterDTO(unique_code=group_id)
        group = next(
            iter(
                self.filter_data(
                    filt=group_filter,
                    key=DataReposity.group_key()
                )
            )
            , None
        )
        return group
    
    def get_unit_by_id(self, unit_id):
        unit_filter = FilterDTO(unique_code=unit_id)
        unit = next(
            iter(
                self.filter_data(
                    filt=unit_filter,
                    key=DataReposity.unit_key()
                )
            )
            , None
        )
        return unit
    
    def update_nomenclature(self, nomenclature: Nomenclature, params):
        ValidatorWrapper.validate_type(nomenclature, Nomenclature, "nomenclature in update_nomenclature")
        name = params['name']
        full_name = params['full_name']
        group_id = params['group_id']
        unit_id = params['unit_id']
        
        if name is not None:
            nomenclature.name = name
        
        if full_name is not None:
            nomenclature.full_name = full_name
        
        if group_id is not None:
            group = self.get_group_by_id(group_id)
            if group is None:
                return {"message": f"Group with id {group_id} is not exist"}
            nomenclature.group = group
            
        if unit_id is not None:
            unit = self.get_unit_by_id(unit_id)
            if unit is None:
                return {"message": f"Unit with id {unit_id} is not exist"}
            nomenclature.unit = unit
            
    
    def update_nomenclature_in_recipes(self, unique_code, params):
        recipes = self.reposity.data[DataReposity.recipe_key()]
        for recipe in recipes:
            self.has_nomenclature(recipe, unique_code, params)
            
            
    
    def update_nomenclature_in_transactions(self, unique_code, params):
        transactions = self.reposity.data[DataReposity.warehouse_transaction_key()]
        for transaction in transactions:
            self.has_nomenclature(transaction, unique_code, params)
    
    def has_nomenclature(self, obj, unique_code, params):
        if hasattr(obj, 'id') and obj.id == unique_code:
            self.update_nomenclature(
                nomenclature=obj,
                params=params
            )
            
        if isinstance(obj, dict):
            for _, value in obj.items():
                self.has_nomenclature(value, unique_code, params)
                
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                self.has_nomenclature(item, unique_code, params)
                
        elif hasattr(obj, '__dict__'):
            for attr_name in vars(obj):
                attr_value = getattr(obj, attr_name)
                self.has_nomenclature(attr_value, unique_code, params)
        
        

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
        
    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)
        match type:
            case EventType.CHANGE_NOMENCLATURE:
                return self.update(params)
            case EventType.DELETE_NOMENCLATURE:
                return self.delete(params)
        return {"Status": "Something went wrong"}