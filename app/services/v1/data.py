import polars as pl
import logging
from sqlalchemy.orm import Session
from app.core.database import crud, connection

logger = logging.getLogger(__name__)

def get_data(table_name: str, session: Session):
    pass

def get_data_csv(file_path: str, 
                 n_limit: int=100000):
    df = pl.read_csv(file_path, separator=',', n_rows=n_limit, ignore_errors=True)

    return df

def get_data_db(table_name: str, 
                session: Session):
    result = crud.get_transaction_data(session)
    return result

def get_data_stream(topic_name: str):
    pass