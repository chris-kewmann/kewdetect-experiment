from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Double
from sqlalchemy.orm import relationship

from app.core.connection.postgres import Base

class Transaction(Base):
    __tablename__ = 'transaction'
    index = Column(Integer, primary_key=True, index=True)
    biaya = Column(Double)
    nilai = Column(Double)