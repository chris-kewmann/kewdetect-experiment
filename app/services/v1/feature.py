import logging
import polars as pl
import pandas as pd
from featurewiz import FeatureWiz
from sqlalchemy.orm import Session

from app.config import config
from app.database.v1.schemas import feature as schema
from app.services.v1.data import get_data_db


logger = logging.getLogger(__name__)

def preprocess():
    pass

def transform():
    pass

def get_features(table_name:str):
    query = f'SELECT * FROM {table_name} limit 1'
    df = pd.read_sql(query, con=config.DB_POSTGRES_URI)
    features = df.columns.tolist()
    result = schema.FeatureList(features=features)
    return result

def select_features(df:pl.DataFrame):
    features = ['biaya', 'nilai']

    df = df.select(pl.col(features))
    df = df.fill_nan(0)
    df = df.fill_null(0)
    return df

# TODO: Research Feature Selection on Unsupervised Data
def select_features_auto(request: schema.FeatureSelectionAuto):
    query = f'SELECT * FROM {request.table_name}'
    df = pd.read_sql(query, con=config.DB_POSTGRES_URI)
    
    # TODO: set label column from request field
    label_column = 'is_outlier'
    feature_columns = [col for col in df.columns if col != label_column]
    X = df[feature_columns]
    y = df[label_column]

    fw = FeatureWiz(corr_limit=0.70, 
                    feature_engg='', 
                    category_encoders='', 
                    dask_xgboost_flag=False, 
                    nrows=None, 
                    verbose=0)
    
    fw.fit(X,y)
    selected_features = fw.features
    result = schema.FeatureList(features=selected_features)
    return result