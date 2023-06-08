import logging
from fastapi import APIRouter, status

from app.database.v1.schemas import feature as schema
from app.services.v1 import feature as service

# Get logger
logger = logging.getLogger(__name__)

# Set router group
router = APIRouter(prefix='/v1/features',
                   responses={500: {'description': 'Internal Server Error'}})

# Endpoints
@router.get(path='/{table_name}',
            status_code=status.HTTP_200_OK,
            summary="Get list of features",
            description="Get list of available features",
            response_model=schema.FeatureList)
async def get_features(table_name: str):
    return service.get_features(table_name)

@router.post(path="/select/auto", 
            status_code=status.HTTP_200_OK,
            summary="Automatic feature selection",
            description="Select feature automatically by algorithm",
            response_model=schema.FeatureList,
            deprecated=True)
async def select_feature_auto(request: schema.FeatureSelectionAuto):
    return service.select_features_auto(request) 

