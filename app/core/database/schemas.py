from typing import Union
from pydantic import BaseModel

class Rule(BaseModel):
    name: str
    description: Union[str, None] = None

class Model(BaseModel):
    id: str
    name: Union[str, None] = None

class Transaction(BaseModel):
    index: str
    biaya: float
    nilai: float

    class Config:
        orm_mode = True