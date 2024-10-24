from pydantic import BaseModel

class FilterDTOModel(BaseModel):
    name: str | None = None
    unique_code: str | None = None
    type: str | None = None