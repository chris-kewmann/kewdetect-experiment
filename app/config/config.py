import os
import logging
import mlflow
from dotenv import load_dotenv
from functools import lru_cache
from func_timeout import func_set_timeout
from pydantic import BaseSettings
load_dotenv()

# Non-variable configuration
logger = logging.getLogger(__name__)

# Base Settings Class
class Settings(BaseSettings):
    # Postgres database variables
    db_postgres_username: str = 'postgres'
    db_postgres_password: str = 'postgres'
    db_postgres_host: str = '127.0.0.1'
    db_postgres_port: int = 5432
    db_postgres_name: str = 'kewdetect'

    # Mlflow variables
    mlflow_host: str = '127.0.0.1'
    mlflow_port: int = 5000
    mlflow_experiment_name: str = 'kewdetectkewdetect_models'

    # Security variables
    encrypt_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Get base settings function
@lru_cache()
def get_settings():
    return Settings()

# Base setting object
settings = get_settings()

# Database Variables
DB_POSTGRES_URI = f'postgresql://{settings.db_postgres_username}:{settings.db_postgres_password}@{settings.db_postgres_host}:{settings.db_postgres_port}/{settings.db_postgres_name}'

# Mlflow Variables
MLFLOW_TRACKING_URI = f'http://{settings.mlflow_host}:{settings.mlflow_port}'

class MlflowSetup:
    """
    This configuration is only set once and will be used several times during the service lifetime
    components:
        - mlflow tracking
    """
    def __init__(self):
        try:
            # self.mlflow_client = None
            self.set_mlflow()

            logging.info("initial config is success!")
        except Exception:
            logging.exception("initial config is failed!")
            exit(1) # exit(4) if want to force stop / prevent gunicorn from reloading

    @func_set_timeout(10)
    def set_mlflow(self):
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

            mlflow.set_experiment(settings.mlflow_experiment_name)

            # self.mlflow_client = mlflow.MlflowClient()
        except Exception:
            logger.critical("failed to connect mlflow")
            raise