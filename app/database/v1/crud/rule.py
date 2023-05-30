from sqlalchemy.orm import Session

from app.database.v1.models import rule as model
from app.database.v1.schemas import rule as schema

def create_rule(db: Session, rule: schema.RuleCreate):
    new_rule = model.Rule(**rule.dict())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

def get_rules(db: Session, limit: int=100):
    return db.query(model.Rule).limit(limit).all()

def get_rule_detail(db: Session, rule_id: int):
    return db.query(model.Rule).filter(model.Rule.id == rule_id).one()

def update_rule(db: Session, rule: schema.RuleUpdate):
    existing_rule = db.query(model.Rule).filter(model.Rule.id == int(rule.id)).one()
    existing_rule.name = rule.name
    existing_rule.condition = rule.condition
    existing_rule.data_source = rule.data_source
    existing_rule.description = rule.description
    existing_rule.operator = rule.operator
    existing_rule.threshold = rule.threshold
    existing_rule.is_active = rule.is_active
    db.commit()
    return rule

def delete_rule(db: Session, rule_id: int):
    db.query(model.Rule).filter(model.Rule.id == rule_id).delete()
    db.commit()
    return rule_id

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