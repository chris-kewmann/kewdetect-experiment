from sqlalchemy.orm import Session
from app.core.database import models, schemas

def get_transaction_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Transaction).offset(skip).limit(limit).all()