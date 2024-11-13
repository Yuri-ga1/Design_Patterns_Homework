from src.emuns.event_types import EventType
from general.abstract_files.abstract_logic import AbstractLogic
from general.exception.Validator_wrapper import ValidatorWrapper

class ObserverService:
    observers = []
    
    @staticmethod
    def add(service: AbstractLogic):
        ValidatorWrapper.validate_type(service, AbstractLogic, "service in ObserverService")
        
        items = list(map(lambda x: type(x).__name__,  ObserverService.observers))
        found = type(service).__name__ in items 
        if not found: 
            ObserverService.observers.append(service)

    @staticmethod
    def raise_event(type: EventType, params):
        statuses = {}
        for instance in ObserverService.observers:
            if instance is not None:
                try:
                    status = instance.handle_event(type, params)
                    statuses[type(instance).__name__] = status
                except Exception:
                    continue
        return statuses
    