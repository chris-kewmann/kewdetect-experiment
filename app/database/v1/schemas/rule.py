from typing import Union, List
from pydantic import BaseModel, Field

class RuleBase(BaseModel):
    name: str = Field(example='rule 1t')
    description: Union[str, None] = Field(default=None, example='catch transaction frequency larger than 10')
    condition: str = Field(example='sum(transaction_count)')
    threshold: float = Field(example='12')
    operator: str = Field(example='>=')
    data_source: str = Field(example='db')
    is_active: bool = Field(example='false')

class RuleCreate(RuleBase):
    pass

class RuleDetail(RuleBase):
    id: Union[str, None] = Field(default=None, example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')
    
    class Config:
        orm_mode = True

class RuleDetailList(BaseModel):
    rules: List[RuleDetail]

class RuleUpdate(RuleDetail):
    pass

class RuleDelete(BaseModel):
    id: str = Field(example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')

class RuleState(BaseModel):
    id: str = Field(example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')
