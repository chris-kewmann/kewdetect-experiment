from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double, ARRAY
from sqlalchemy.orm import relationship

from app.core.connection.postgres import Base

class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    algorithm = Column(String)
    mlflow_run_id = Column(String)
    data_table_name = Column(String)
    data_columns = Column(ARRAY(String))
    rule_set_id = Column(Integer)
    is_active = Column(Boolean, default=False)