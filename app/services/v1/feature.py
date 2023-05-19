import logging
import polars as pl

logger = logging.getLogger(__name__)

def preprocess():
    pass

def select_features(df:pl.DataFrame):
    features = ['biaya', 'nilai']

    df = df.select(pl.col(features))
    df = df.fill_nan(0)
    df = df.fill_null(0)
    return df