from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double
from sqlalchemy.orm import relationship

from app.core.connection.postgres import Base

class Rule(Base):
    __tablename__ = 'rule'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    condition = Column(String)
    threshold = Column(Double)
    operator = Column(String)
    data_source = Column(String)
    is_active = Column(Boolean, default=False)