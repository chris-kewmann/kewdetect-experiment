import mlflow
import polars as pl
from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.lof import LOF
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from mlflow.models.signature import infer_signature

from app.services.v1.data import get_data_csv
from app.services.v1.feature import select_features

def create(run_name:str, mlflow_registered_model_name:str, model_name:str, data_source:str='csv'):
    with mlflow.start_run(run_name=run_name):
        mlflow.sklearn.autolog(registered_model_name=mlflow_registered_model_name)
        
        # Retrieve and read data
        if data_source == 'csv':
            df = get_data_csv(file_path='app/sample/data_trx.csv', n_limit=1000)

        # Select features
        df = select_features(df)

        # Convert to numpy before feed to model
        df = df.to_pandas()

        # Pick one model
        model = select_model(model_name=model_name,
                            contamination=0.1,
                            n_jobs=-1)

        df['label'] = model.fit_predict(df)

        signature = infer_signature(df, df['label'])
        mlflow.sklearn.log_model(model, "model", signature=signature)

def predict(model_name:str, outlier_percentage:float=0.1, data_source:str='csv'):
    # Retrieve and read data
    if data_source == 'csv':
        df = get_data_csv(file_path='app/sample/data_trx.csv')

    # Select features
    df = select_features(df)

    # Convert to numpy before feed to model
    df = df.to_pandas()

    # Pick one model
    model = select_model(model_name=model_name, 
                         contamination=outlier_percentage, 
                         n_jobs=-1)

    result = model.fit_predict(df)

    return result, model

def select_model(model_name:str='lof', backend:str='sklearn', **kwargs):
    if model_name == 'lof':
        #model = LOF(**kwargs)
        model = LocalOutlierFactor(**kwargs)
    elif model_name == 'isof':
        model = IsolationForest(**kwargs)
    elif model_name == 'mcd':
        model = EllipticEnvelope(**kwargs)
    # elif model_name == 'ecod':
    #     model = ECOD(**kwargs)
    # elif model_name == 'copod':
    #     model = COPOD(**kwargs)

    return model