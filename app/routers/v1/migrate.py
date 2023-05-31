
from fastapi import APIRouter, status
from app.core import utils

# Set router group
router = APIRouter(prefix='/v1/migrate',
                   responses={500: {'description': 'Internal Server Error'}})

# Endpoints
@router.post(path="/", 
            status_code=status.HTTP_201_CREATED)
async def migrate():
    utils.create_migration()
    return {"message": "OK"}