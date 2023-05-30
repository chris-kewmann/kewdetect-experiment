from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException, status
from app.config import config
from app.core.connection.postgres import engine
from app.database.v1.models.rule import Base as BaseRule
from app.database.v1.models.transaction import Base as BaseTransaction


"""
def fetch_mlflow_data(run_id:str):
    data = app.conf.mlflow_client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in app.conf.mlflow_client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts
"""

def create_migration():
    # Create table if not exist
    BaseRule.metadata.drop_all(bind=engine)
    BaseRule.metadata.create_all(bind=engine)
    
    BaseTransaction.metadata.drop_all(bind=engine)
    BaseTransaction.metadata.create_all(bind=engine)

def encrypt(inp: str):
    try:
        if not isinstance(inp, bytes):
            inp = inp.encode(encoding='utf-8')
        f = Fernet(config.ENCRYPT_KEY)
        result = f.encrypt(inp).decode()
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')

    return result

def decrypt(inp: str):
    try:
        f = Fernet(config.ENCRYPT_KEY)
        result = f.decrypt(inp).decode(encoding='utf-8')
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')
    
    return result
