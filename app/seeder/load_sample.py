import pandas as pd
from sqlalchemy import create_engine

PG_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/kewdetect'
PG_TABLE_NAME = 'transaction'

DATA_PATH = './sample/data_trx.csv'

engine = create_engine(PG_DATABASE_URI)

df = pd.read_csv(DATA_PATH)
df = df[['biaya', 'nilai']]
df.to_sql(PG_TABLE_NAME, con=engine)

