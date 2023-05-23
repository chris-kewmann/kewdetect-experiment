import logging
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.services.v1.data import get_data_csv, get_data_db
from app.core.database import connection

# Get logger
logger = logging.getLogger(__name__)

# Request schemas
class GetData(BaseModel):
    source: str = Field(default=None, example='csv')

# Set router group
router = APIRouter(prefix='/v1/data',
                   tags=["data"],
                   responses={500: {'description': 'Internal Server Error'}})
# Endpoints
@router.get(path="/", 
            status_code=status.HTTP_200_OK,
            summary="Get sample data",
            description="Retrieve data")
async def get_data(request: GetData, session: Session=Depends(connection.get_session)):
    if request.source == 'csv':
        df = get_data_csv(file_path='app/seeder/sample/data_trx.csv')
        df = df.limit(10).to_dicts()
    elif request.source == 'db':
        df = get_data_db(table_name='transaction', session=session)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'source {request.source} is not recognized')

    return df

@router.post(path="/", 
            status_code=status.HTTP_200_OK,
            summary="Add data source",
            description="Add and set data source")
async def add_data():
    pass

@router.delete(path="/",
               status_code=status.HTTP_200_OK,
               summary="Delete data source",
               description="Remove data source")
async def delete_data():
    pass

@router.put(path="/", 
            status_code=status.HTTP_200_OK,
            summary="Edit data source",
            description="Remove data source")
async def edit_data():
    pass