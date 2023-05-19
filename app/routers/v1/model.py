import logging
import mlflow
from fastapi import APIRouter
from mlflow.models.signature import infer_signature

from app.services.v1 import model

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/v1/models',
                   tags=["models"],
                   responses={500: {'description': 'Internal Server Error'}})

@router.get("/")
async def get_models():
    return ['model-a', 'model-b']

@router.post("/")
async def create_model():
    run_name = 'my-run'
    mlflow_registered_model_name='my-model'
    model_name = 'lof'
    data_source = 'csv'

    model.create(run_name, mlflow_registered_model_name, model_name, data_source)

    return {'message': 'OK'}

@router.delete("/")
async def delete_model():
    pass

@router.put("/")
async def edit_model():
    pass

@router.post("/predict")
async def predict():
    result, _ = model.predict(model_name='ecod', 
                           outlier_percentage=0.1, 
                           data_source='csv')

    response = {
        'predicted' : result.tolist()[:10]
    }

    return response

@router.post("/deploy")
async def deploy():
    pass

@router.post("/undeploy")
async def undeploy():
    pass
