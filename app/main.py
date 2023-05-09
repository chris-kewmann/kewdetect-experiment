import os
import mlflow
import logging 
from datetime import datetime
from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import model, data

from dotenv import load_dotenv
load_dotenv()

async def setup_logging():
    CONFIG_DIR = "app/config"
    LOG_DIR = "app/logs"

    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get('dev', "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_logging()

    # # Set logger
    # # instantiate logger
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)

    # # define handler and formatter
    # handler = logging.StreamHandler()
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # # add formatter to handler
    # handler.setFormatter(formatter)

    # # add handler to logger
    # logger.addHandler(handler)

    # Set Mlflow
    # mlflow.set_tracking_uri('127.0.0.1:5000')
    # mlflow.autolog()

    yield

    # TODO: Clean up method before shutting down service
    # db.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router=model.router,
                   tags=["Models"],
                   responses={500: {'description': 'internal server error'}})

@app.get("/")
async def root():
    return {'hello': 'world'}