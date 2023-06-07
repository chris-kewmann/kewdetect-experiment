import connectorx
import logging
import mlflow
import polars as pl
from fastapi import HTTPException, status
from mlflow import MlflowClient
from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.lof import LOF
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from mlflow.models.signature import infer_signature
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from pprint import pprint

from app.config import config
from app.core.utils import encrypt, decrypt, orm_to_dict
from app.database.v1.crud import model as crud
from app.database.v1.schemas import model as schema
from app.services.v1.data import get_data_csv
from app.services.v1.feature import select_features

logger = logging.getLogger(__name__)
logger.debug(connectorx.__version__)

def create_model(db: Session, request: schema.ModelCreate):
    try:
        logger.info('creating model')

        with mlflow.start_run(run_name=request.name) as run:
            mlflow.sklearn.autolog(registered_model_name=request.name)

            # TODO: DEPCREATED 
            # df = get_data_csv(file_path='app/seeder/sample/data_trx.csv', n_limit=1000)
            # df = select_features(df)

            # Read data 
            logger.info('read data from database')
            columns = ', '.join(request.data_columns)
            query = f'SELECT {columns} FROM {request.data_table_name}'
            df = pl.read_database(query=query,
                                connection_uri=config.DB_POSTGRES_URI)

            # Convert to pandas
            df = df.to_pandas().sample(100)
            df.fillna(0, inplace=True)

            # Pick one model
            model = select_model(algorithm=request.algorithm,
                                contamination=0.1,
                                n_jobs=-1)

            logger.info('feed data to model')
            df['label'] = model.fit_predict(df)

            logger.info('log model to mlflow')
            signature = infer_signature(df[request.data_columns], df['label'])
            mlflow.sklearn.log_model(model, "model", signature=signature)
            logger.info('log model to mlflow success')

            mlflow_run_id = run.info.run_id


        mlflow_client = MlflowClient()
        for mod in mlflow_client.search_registered_models(filter_string=f"name='{request.name}'"):
            print(type(mod))
            pprint(dict(mod), indent=4)

        request.rule_set_id = int(decrypt(request.rule_set_id))
        result = crud.create_model(db, request, mlflow_run_id)
        result.id = encrypt(result.id)
        result.rule_set_id = encrypt(request.rule_set_id)
        logger.info(f'create model {result.id} success')
    except Exception:
        logger.exception('create model failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return result

def get_models(db: Session, limit: int):
    try:
        mlflow_info = dict()
        mlflow_client = MlflowClient()
        for model in mlflow_client.search_registered_models():
            mlflow_info[model.latest_versions[0].run_id] = model
        
        logger.info(mlflow_info)

        models = crud.get_models(db, limit=limit)
        result = list()
        for i in range(len(models)):
            model = orm_to_dict(models[i])
            model['id'] = encrypt(model['id'])
            model['rule_set_id'] = encrypt(model['rule_set_id'])
            mlflow_metadata = mlflow_info.get(model['mlflow_run_id'], dict())
            model['mlflow_metadata'] = mlflow_metadata 
            if mlflow_metadata:
                model['mlflow_metadata'] = mlflow_metadata.latest_versions[0]
            result.append(model)

        response = schema.ModelDetailList(models=result)
    except Exception:
        logger.exception('get models failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response 

def get_model_detail(db: Session, model_id: str):
    try:
        logger.error(model_id)
        model_id = int(decrypt(model_id))
        model = orm_to_dict(crud.get_model_detail(db, model_id=model_id))
        run_id = model['mlflow_run_id']

        mlflow_client = MlflowClient()
        data = mlflow_client.get_run(run_id).data
        tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
        artifacts = [f.path for f in mlflow_client.list_artifacts(run_id, "model")]
        logger.debug(tags)
        logger.debug(artifacts)
        logger.debug(data.params)
        logger.debug(data.metrics)
        #return data.params, data.metrics, tags, artifacts
    except Exception:
        logger.exception('get model detail failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    del model['algorithm']
    return dict(**tags, **data.params, **data.metrics, **model)

def predict(request: schema.ModelPredict):
    try:
        # Load Model
        model_uri = f'runs:/{request.run_id}/model'
        model = mlflow.sklearn.load_model(model_uri=model_uri)
    
        features = model.feature_names_in_
        logger.info(features)
        logger.info(request.columns)
        if set(features) != set(request.columns):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                                detail=f'required features : [{" | ".join(features)}] ----- given : [{" | ".join(request.columns)}]')
        
        # Read data 
        logger.info('read data from database')
        columns = ', '.join(request.columns)
        
        #query = f'SELECT {columns} FROM {request.data_table_name}'
        query = f'SELECT {columns} FROM {request.table_name}'
        df = pl.read_database(query=query,
                            connection_uri=config.DB_POSTGRES_URI)

        # Convert to pandas
        df = df.to_pandas().sample(100)
        df.fillna(0, inplace=True)

        result = model.fit_predict(df)
    except Exception:
        logger.exception('model predict failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {'result': result.tolist()}

def update_model(db: Session, request: schema.ModelDetail):
    try:
        encrypted_model_id = request.id
        encrypted_rule_set_id = request.rule_set_id
        logger.info(f'updating model {encrypted_model_id}')
        
        request.id = int(decrypt(encrypted_model_id))
        request.rule_set_id = int(decrypt(encrypted_rule_set_id))
        result = crud.update_model(db, request)
        result.id = encrypted_model_id
        result.rule_set_id = encrypted_rule_set_id

        logger.info(f'update rule {encrypted_model_id} success')
    except NoResultFound:
        logger.error(f'update rule {encrypted_model_id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='model not found')
    except Exception:
        logger.exception('update model failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return result

def delete_model(db: Session, request: schema.ModelDelete):
    try:
        logger.info(f'deleting model {request.id}')
        model_id = int(decrypt(request.id))
        deleted_model = crud.delete_model(db, model_id)

        mlflow_run_id = deleted_model.mlflow_run_id
        mlflow_client = MlflowClient()
        mlflow_client.delete_run(mlflow_run_id)
    except NoResultFound:
        logger.error(f'delete rule {request.id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='model not found')
    except Exception:
        logger.exception('delete model failed')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return deleted_model

def select_model(algorithm:str='lof', backend:str='sklearn', **kwargs):
    if algorithm == 'lof':
        #model = LOF(**kwargs)
        model = LocalOutlierFactor(**kwargs)
    elif algorithm == 'isof':
        model = IsolationForest(**kwargs)
    elif algorithm == 'mcd':
        model = EllipticEnvelope(**kwargs)
    # elif model_name == 'ecod':
    #     model = ECOD(**kwargs)
    # elif model_name == 'copod':
    #     model = COPOD(**kwargs)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='invalid algorithm')

    return model