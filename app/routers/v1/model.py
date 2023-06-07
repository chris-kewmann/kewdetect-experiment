import logging
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Union

from app.core.connection.postgres import get_session
from app.services.v1 import model as service
from app.database.v1.schemas import model as schema

# Get logger
logger = logging.getLogger(__name__)

# Set router group
router = APIRouter(prefix='/v1/models',
                   responses={500: {'description': 'Internal Server Error'}})

# Endpoints
@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             summary="Create model",
             description="Create new model",
             response_model=schema.ModelDetail)
async def create_model(request: schema.ModelCreate, session: Session = Depends(get_session)):
    
    valid_model_algorithms = ['lof', 'isof', 'mcd']
    if request.algorithm not in valid_model_algorithms:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'algorithm {request.algorithm} is not supported')
    
    return service.create_model(session, request)

@router.get(path="/", 
            status_code=status.HTTP_200_OK,
            summary="Get models",
            description="Retrieve all models",
            response_model=schema.ModelDetailList)
async def get_models(limit: Union[int, None] = None, session: Session = Depends(get_session)):
    return service.get_models(session, limit)

@router.get(path="/{model_id:path}", 
            status_code=status.HTTP_200_OK,
            summary="Get model detail",
            description="Get model detail and information")
async def get_model_detail(model_id: str, session: Session = Depends(get_session)):
    return service.get_model_detail(session, model_id)

@router.post(path="/predict", 
             status_code=status.HTTP_200_OK,
             summary="Predict",
             description="Predict on the given data")
async def predict(request: schema.ModelPredict):
    return service.predict(request)

@router.delete(path="/", 
               status_code=status.HTTP_200_OK,
               summary="Delete existing model",
               response_model=schema.ModelDetail)
async def delete_model(request: schema.ModelDelete, session: Session = Depends(get_session)):
    return service.delete_model(session, request)

@router.put(path="/",
            status_code=status.HTTP_200_OK,
            summary="Edit model",
            description="Edit existing model configuration",
            response_model=schema.ModelDetail)
async def edit_model(request: schema.ModelDetail, session: Session = Depends(get_session)):
    return service.update_model(session, request)


"""
@router.post(path="/deploy", 
             status_code=status.HTTP_200_OK)
async def deploy():
    pass

@router.post(path="/undeploy", 
             status_code=status.HTTP_200_OK)
async def undeploy():
    pass
"""