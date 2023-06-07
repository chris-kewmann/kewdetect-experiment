from copy import deepcopy
from sqlalchemy.orm import Session

from app.database.v1.models import rule as model
from app.database.v1.schemas import rule as schema

def create_rule(db: Session, request: schema.RuleCreate):
    new_rule = model.Rule(**request.dict())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

def get_rules(db: Session, limit: int=100):
    return db.query(model.Rule).limit(limit).all()

def get_rule_detail(db: Session, rule_id: int):
    return db.query(model.Rule).filter(model.Rule.id == rule_id).one()

def update_rule(db: Session, request: schema.RuleUpdate):
    existing_rule = db.query(model.Rule).filter(model.Rule.id == int(request.id)).one()
    existing_rule.name = request.name
    existing_rule.condition = request.condition
    existing_rule.data_source = request.data_source
    existing_rule.description = request.description
    existing_rule.operator = request.operator
    existing_rule.threshold = request.threshold
    existing_rule.is_active = request.is_active
    db.commit()
    return existing_rule

def delete_rule(db: Session, rule_id: int):
    obj = db.query(model.Rule).filter(model.Rule.id == rule_id)
    result = deepcopy(obj.one())
    obj.delete()
    db.commit()
    return result

def activate_rule(db: Session, rule_id: str):
    rule = db.query(model.Rule).filter(model.Rule.id == rule_id).one()
    rule.is_active = True
    db.commit()
    db.refresh(rule)
    return rule
    
def deactivate_rule(db: Session, rule_id: str):
    rule = db.query(model.Rule).filter(model.Rule.id == rule_id).one()
    rule.is_active = False
    db.commit()
    db.refresh(rule)
    return rule 