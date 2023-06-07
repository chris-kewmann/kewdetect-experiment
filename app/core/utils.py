import hashlib
import logging
from base64 import b64encode, b64decode
#from cryptography.fernet import Fernet, InvalidToken
from Crypto.Cipher import AES
from Crypto import Random
from fastapi import HTTPException, status
from sqlalchemy import inspect

from app.config import config
from app.core.connection.postgres import engine
from app.database.v1.models.model import Base as BaseModel
from app.database.v1.models.rule import Base as BaseRule
from app.database.v1.models.transaction import Base as BaseTransaction

# Non-variable configuration
logger = logging.getLogger(__name__)

# AES variables
AES_KEY = config.settings.private_key
BLOCK_SIZE = 16
PRIVATE_KEY = hashlib.sha256(AES_KEY.encode("utf-8")).digest()
# Custom AES utils function
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def create_migration():
    # Create table if not exist
    logger.info('migrating model table')
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)

    logger.info('migrating rule table')
    BaseRule.metadata.drop_all(bind=engine)
    BaseRule.metadata.create_all(bind=engine)
    
    logger.info('migrating transaction table')
    BaseTransaction.metadata.drop_all(bind=engine)
    BaseTransaction.metadata.create_all(bind=engine)

def encrypt(inp: any):
    try:
        if not isinstance(inp, str):
            inp = str(inp)
        
        inp = pad(inp).encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(PRIVATE_KEY, AES.MODE_CBC, iv)
        result =  b64encode(iv + cipher.encrypt(inp))
    except Exception as e:
        logger.exception('encrypt failed')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'encrypt failed : {str(e)}')
    
    return result

def decrypt(inp: str):
    try:
        inp = b64decode(inp)
        iv = inp[:16]
        cipher = AES.new(PRIVATE_KEY, AES.MODE_CBC, iv)
        result = unpad(cipher.decrypt(inp[16:]))
    except Exception as e:
        logger.exception('decrypt failed')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'decrypt failed : {str(e)}')
    
    return result

def orm_to_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# TODO: DEPRECATED
# def encrypt(inp: int):
#     try:
#         if not isinstance(inp, str):
#             inp = str(inp)
#         if not isinstance(inp, bytes):
#             inp = inp.encode(encoding='utf-8')
#         f = Fernet(config.settings.private_key)
#         result = f.encrypt(inp).decode()
#     except InvalidToken:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')

#     return result

# def decrypt(inp: str):
#     try:
#         f = Fernet(config.settings.private_key)
#         result = f.decrypt(inp).decode(encoding='utf-8')
#     except InvalidToken:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f'invalid id')
    
#     return result