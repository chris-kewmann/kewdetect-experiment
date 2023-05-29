import os
import logging
import mlflow
from dotenv import load_dotenv
from func_timeout import func_set_timeout
load_dotenv()

# Set all configuration variables here
# Database Variables
DB_POSTRES_USERNAME = os.getenv('DB_POSTGRES_USERNAME')
DB_POSTRES_PASSWORD = os.getenv('DB_POSTGRES_PASSWORD')
DB_POSTGRES_HOST = os.getenv('DB_POSTGRES_HOST')
DB_POSTGRES_PORT = os.getenv('DB_POSTGRES_PORT')
DB_POSTGRES_NAME = os.getenv('DB_POSTGRES_NAME')
DB_POSTGRES_URI = f'postgresql://{DB_POSTRES_USERNAME}:{DB_POSTRES_PASSWORD}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}/{DB_POSTGRES_NAME}'

# DB_MYSELF_USERNAME =
# DB_MYSQL_PASSWORD =
# DB_MYSQL_HOST =
# DB_MYSEL_NAME =

# Elastic Search Variables
# ES_HOST =
# ES_PORT =

# Mlflow Variables
MLFLOW_HOST = os.getenv('MLFLOW_HOST')
MLFLOW_PORT = os.getenv('MLFLOW_PORT')
MLFLOW_TRACKING_URI = f'http://{MLFLOW_HOST}:{MLFLOW_PORT}'
MLFLOW_EXPERIMENT_NAME = os.getenv('MLFLOW_EXPERIMENT_NAME')

# Security Variables
ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')

# Non-variable configuration
logger = logging.getLogger(__name__)

class Config:
    """
    This configuration is only set once and will be used several times during the service lifetime
    components:
        - mlflow tracking
    """
    def __init__(self):
        try:
            self.mlflow_client = None
            self.set_mlflow()

            logging.info("initial config is success!")
        except Exception:
            logging.exception("initial config is failed!")
            exit(1) # exit(4) if want to force stop / prevent gunicorn from reloading

    @func_set_timeout(10)
    def set_mlflow(self):
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

            mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

            self.mlflow_client = mlflow.MlflowClient()
        except Exception:
            logger.critical("failed to connect mlflow")
            raise

