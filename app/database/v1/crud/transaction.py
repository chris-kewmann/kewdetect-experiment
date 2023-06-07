from sqlalchemy.orm import Session
from app.database.v1.models import transaction as model
from app.database.v1.schemas import transaction as schema

def get_transaction_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(model.Transaction).offset(skip).limit(limit).all()