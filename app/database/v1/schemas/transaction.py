from typing import Union
from pydantic import BaseModel

class Model(BaseModel):
    id: str
    name: Union[str, None] = None

class Transaction(BaseModel):
    index: str
    biaya: float
    nilai: float

    class Config:
        orm_mode = True