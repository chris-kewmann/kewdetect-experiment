from pydantic import BaseModel, Field
from typing import List

class FeatureSelectionAuto(BaseModel):
    table_name: str = Field(example='sample_dataset')

class FeatureList(BaseModel):
    features: List[str] = Field(example=['index', 'nilai', 'biaya'])