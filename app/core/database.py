import logging
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

from app.config import config

logger = logging.getLogger(__name__)
logger.info(f'psycopg2 version : {psycopg2.__version__}')

SQLALCHEMY_DATABASE_URL = config.DB_POSTGRES_URI

"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

CreateSession = sessionmaker(autocommit=False, 
                            autoflush=False,
                            bind=engine)

Base = declarative_base()
"""