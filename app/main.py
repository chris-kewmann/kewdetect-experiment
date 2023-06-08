import os
import mlflow
import logging
import uvicorn
from datetime import datetime
from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.v1 import data, feature, model, rule, migrate
from app.config.config import MlflowSetup

from dotenv import load_dotenv
load_dotenv()

async def setup_logging():
    CONFIG_DIR = "app/config"
    LOG_DIR = "app/logs"

    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get('dev', "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute following methods at starting service time
    await setup_logging()
    mlflow_setup = MlflowSetup()

    yield

    # TODO: Clean up method before shutting down service
    # db.close()

logger = logging.getLogger(__name__)
logger.debug(uvicorn.__version__)

try:
    app = FastAPI(
        lifespan=lifespan,
        title="KewDetect",
        description="Kewdetect Main Service",
        version="0.0.1",
        terms_of_service="https://www.kewmann.com/",
        contact={
            "name": "Kewdetect Developer",
            "url": "https://www.kewmann.com/company/contacts",
            "email": "dev@kewmann.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
    )

    app.include_router(router=data.router,
                    tags=["Data"],
                    responses={500: {'description': 'Internal Server Error'}})
    
    app.include_router(router=feature.router,
                    tags=["Features"],
                    responses={500: {'description': 'Internal Server Error'}})
    
    app.include_router(router=model.router,
                    tags=["Models"],
                    responses={500: {'description': 'Internal Server Error'}})
    
    app.include_router(router=rule.router,
                    tags=["Rules"],
                    responses={500: {'description': 'Internal Server Error'}})
    
    app.include_router(router=migrate.router,
                    tags=["Migration"],
                    responses={500: {'description': 'Internal Server Error'}})
    
    logger.info('application is ready and serving')
except Exception as e:
    logger.exception('start service failed')