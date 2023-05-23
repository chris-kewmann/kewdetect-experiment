import logging
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.services.v1 import model

# Get logger
logger = logging.getLogger(__name__)

# Request schemas
class GetModel(BaseModel):
    name: str = Field(default=None, example='fraud-model-alfa')
    version: str = Field(default=None, example='1.0.1')
    limit: int = Field(default=10, example=15)

class CreateModel(BaseModel):
    name: str
    run_name: str
    mlflow_registered_model_name: str
    data_source: str = Field(default='csv', include=['csv', 'database'])

class DeleteModel(BaseModel):
    name: str
    model_id: str

# Set router group
router = APIRouter(prefix='/v1/models',
                   tags=["models"],
                   responses={500: {'description': 'Internal Server Error'}})

# Endpoints
@router.get(path="/", 
            status_code=status.HTTP_200_OK,
            summary="Get model(s) information(s)",
            description="Retrieve a list of model(s) with its attribute & detail")
async def get_models(request: GetModel) -> List[str]:
    return ['model-a', 'model-b']

@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             summary="Create new model")
async def create_model(request: CreateModel):
    run_name = 'my-run'
    mlflow_registered_model_name='my-model'
    model_name = 'lof'
    data_source = 'csv'

    valid_model_names = ['lof', 'if']
    if model_name not in valid_model_names:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'model {model_name} is not supported')
    model.create(run_name, mlflow_registered_model_name, model_name, data_source)

    return {'message': 'OK'}

@router.delete(path="/", 
               status_code=status.HTTP_200_OK,
               summary="Delete existing model")
async def delete_model(request: DeleteModel):
    pass

@router.put(path="/",
            status_code=status.HTTP_200_OK,
            summary="Edit model",
            description="Edit existing model configuration")
async def edit_model():
    pass

@router.post(path="/predict", 
             status_code=status.HTTP_200_OK)
async def predict():
    result, _ = model.predict(model_name='ecod', 
                           outlier_percentage=0.1, 
                           data_source='csv')

    response = {
        'predicted' : result.tolist()[:10]
    }

    return response

@router.post(path="/deploy", 
             status_code=status.HTTP_200_OK)
async def deploy():
    pass

@router.post(path="/undeploy", 
             status_code=status.HTTP_200_OK)
async def undeploy():
    pass
