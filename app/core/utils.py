from cryptography.fernet import Fernet, InvalidToken
from fastapi import HTTPException, status
from app.config import config
from app.core.connection.postgres import engine
from app.database.v1.models.rule import Base as BaseRule
from app.database.v1.models.transaction import Base as BaseTransaction

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
        f = Fernet(config.settings.encrypt_key)
        result = f.encrypt(inp).decode()
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')

    return result

def decrypt(inp: str):
    try:
        f = Fernet(config.settings.encrypt_key)
        result = f.decrypt(inp).decode(encoding='utf-8')
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')
    
    return result
