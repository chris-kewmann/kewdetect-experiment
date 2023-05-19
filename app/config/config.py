import os
import logging
import mlflow
from dotenv import load_dotenv
from func_timeout import func_set_timeout
load_dotenv()

# Set all configuration variables here
# Database Variables
DB_POSTGRES_URI = os.getenv('DB_POSTGRES_URI')
# DB_MYSQL_URI =

# Elastic Search Variables
# ES_HOST =
# ES_PORT =

# Mlflow Variables
MLFLOW_HOST = '127.0.0.1'
MLFLOW_PORT = 5000
MLFLOW_TRACKING_URI = f'http://{MLFLOW_HOST}:{MLFLOW_PORT}'
MLFLOW_EXPERIMENT_NAME = 'kewdetect_models'

# Non-variable configuration
logger = logging.getLogger(__name__)

class Config:

    def __init__(self):
        try:
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

