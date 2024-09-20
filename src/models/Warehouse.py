from general.abstract_files.abstract_model import AbstractReference

class WarehouseModel(AbstractReference):
    __address: str = ""

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value.strip()
        
    def __eq__(self, other):
        if isinstance(other, WarehouseModel):
            return self.__address == other.address
        return NotImplemented