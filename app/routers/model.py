import logging
from fastapi import APIRouter

logging = logging.getLogger(__name__)

router = APIRouter()

@router.get("/models/")
async def get_models():
    return ['model-a', 'model-b']
