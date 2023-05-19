import logging
from fastapi import APIRouter

from app.services.v1.data import get_data_csv

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/v1/data',
                   tags=["data"],
                   responses={500: {'description': 'Internal Server Error'}})

@router.get("/")
async def get_data():
    df = get_data_csv(file_path='app/sample/data_trx.csv')

    return df.limit(10).to_dicts()

@router.post("/")
async def add_data():
    pass

@router.delete("/")
async def delete_data():
    pass

@router.put("/")
async def edit_data():
    pass