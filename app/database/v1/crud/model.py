from copy import deepcopy
from sqlalchemy.orm import Session

from app.database.v1.models import model as model
from app.database.v1.schemas import model as schema

def create_model(db: Session, obj: schema.ModelCreate, mlflow_run_id: str):
    new_model = model.Model(**obj.dict(), mlflow_run_id=mlflow_run_id)
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

def get_models(db: Session, limit=int):
    return db.query(model.Model).limit(limit).all()

def get_model_detail(db: Session, model_id: int):
    return db.query(model.Model).filter(model.Model.id == model_id).one()

def update_model(db: Session, request: schema.ModelDetail):
    existing_model = db.query(model.Model).filter(model.Model.id == int(request.id)).one()
    existing_model.id = request.id
    existing_model.name = request.name
    existing_model.algorithm = request.algorithm
    existing_model.mlflow_run_id = request.mlflow_run_id
    existing_model.data_table_name = request.data_table_name
    existing_model.data_columns = request.data_columns
    existing_model.rule_set_id = request.rule_set_id
    existing_model.is_active = request.is_active
    db.commit()
    return existing_model
    

def delete_model(db: Session, model_id: int):
    obj = db.query(model.Model).filter(model.Model.id == model_id)
    deleted_model = deepcopy(obj.one()) 
    obj.delete()
    db.commit()
    return deleted_model