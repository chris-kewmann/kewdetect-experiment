import polars as pl

from fastapi import Depends
#from app.core.database import CreateSession

# def get_session():
#     session = CreateSession()
#     try:
#         yield session
#     finally:
#         session.close()

def get_data(table_name: str):
    #session = Depends(get_session())
    pass

def get_data_csv(file_path: str, 
                 n_limit: int=100000):
    df = pl.read_csv(file_path, separator=',', n_rows=n_limit, ignore_errors=True)

    return df

def get_data_db(table_name: str):
    pass

def get_data_stream(topic_name: str):
    pass