import logging
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

from app.config import config

# Get Logger
logger = logging.getLogger(__name__)
logger.info(f'psycopg2 version : {psycopg2.__version__}')

# Create sqalchemy base model
Base = declarative_base()

# Create session maker
SQLALCHEMY_DATABASE_URL = config.DB_POSTGRES_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

CreateSession = sessionmaker(autocommit=False, 
                            autoflush=False,
                            bind=engine)

# Creating new database session
async def get_session():
    logger.info('Creating new database session...')
    session = CreateSession()
    try:
        logger.info('New database session is created...')
        yield session
    finally:
        logger.info('Closing database session...')
        session.close()