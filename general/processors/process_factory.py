from general.exception.Validator_wrapper import ValidatorWrapper
from general.exception.exceptions import NotFoundException

class ProcessFactory:
    __processes = {}

    def set_process(self, process_name: str, process_class):
        ValidatorWrapper.validate_type(process_name, str, "process_name in ProcessFactory")
        self.__processes[process_name] = process_class

    def get_process(self, process_name: str):
        """Возвращает экземпляр зарегистрированного процесса."""
        process_class = self.__processes.get(process_name)
        if not process_class:
            raise NotFoundException(f"{process_name}")
        return process_class()