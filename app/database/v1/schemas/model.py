from typing import Union, List
from pydantic import BaseModel, Field

class ModelBase(BaseModel):
    name: str = Field(example='model try-1')
    algorithm: str = Field(example='lof')
    data_table_name: str = Field(example='sample_dataset')
    data_columns: List[str] = Field(example='["biaya", "nilai"]')
    rule_set_id: str = Field(example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')
    is_active: bool = Field(example='false')

class ModelCreate(ModelBase):
    pass

class ModelDetail(ModelBase):
    id: Union[str, None] = Field(default=None, example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')
    mlflow_run_id: str = Field(example='6fb2cd809a1f48f08c539448013ba73c')
    
    class Config:
        orm_mode = True

class ModelDetailList(BaseModel):
    models: List[ModelDetail]

class ModelPredict(BaseModel):
    run_id: str = Field(example='6fb2cd809a1f48f08c539448013ba73c')
    table_name: str = Field(example='sample_dataset')
    columns: list = Field(example=['biaya', 'nilai'])

class ModelDelete(BaseModel):
    id: str = Field(example='zmtRRQvcuB7WUX0rlHkd/DYaB2vdeZox5wXWcO6MK7w=')