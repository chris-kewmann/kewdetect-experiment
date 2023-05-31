import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from app.core.utils import encrypt, decrypt
from app.database.v1.schemas import rule as schema
from app.database.v1.crud import rule as crud

logger = logging.getLogger(__name__)

def create_rule(db: Session, rule: schema.RuleCreate):
    logger.info('creating rules')

    result = crud.create_rule(db, rule)
    result.id = encrypt(str(result.id))

    logger.info(f'create rule {result.id} success')
    return result

def get_rules(db: Session, limit: int = 100):
    logger.info('getting rules')
    rules = crud.get_rules(db, limit=limit)
    for rule in rules:
        rule.id = encrypt(str(rule.id))

    logger.info('get all rules success')
    result = schema.RuleDetailList(rules=rules)
    return result

def get_rule_detail(db: Session, rule_id: str):
    try:
        logger.info(f'getting rule detail {rule_id}')

        decrypted_rule_id = int(decrypt(rule_id))
        result = crud.get_rule_detail(db, rule_id=decrypted_rule_id)
        result.id = rule_id

        logger.info(f'get rule detail {rule_id} success')
    except NoResultFound:
        logger.info(f'get rule detail {rule_id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')

    return result

def update_rule(db: Session, rule: schema.RuleUpdate):
    try:
        encrypted_rule_id = rule.id
        logger.info(f'updating rule {encrypted_rule_id}')
        
        rule.id = decrypt(encrypted_rule_id)
        result = crud.update_rule(db, rule)
        result.id = encrypted_rule_id

        logger.info(f'update rule {encrypted_rule_id} success')
    except NoResultFound:
        logger.info(f'update rule {encrypted_rule_id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    
    return result

def delete_rule(db: Session, rule_id: str):
    logger.info(f'deleting rule {rule_id}')

    decrypted_rule_id = int(decrypt(rule_id))
    deleted_rule_id = crud.delete_rule(db, decrypted_rule_id)
    deleted_rule_id = encrypt(str(deleted_rule_id))
    result = schema.RuleDelete(id=deleted_rule_id)

    logger.info(f'delete rule {rule_id} success')
    return result

def activate_rule(db: Session, rule_id: str):
    try:
        logger.info(f'activating rule {rule_id}')

        decrypted_rule_id = int(decrypt(rule_id))
        result = crud.activate_rule(db, decrypted_rule_id)
        result.id = decrypted_rule_id

        logger.info(f'activate rule {rule_id} success')
    except NoResultFound:
        logger.info(f'activate rule {rule_id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    
    return result

def deactivate_rule(db: Session, rule_id: str):
    try:
        logger.info(f'deactivating rule {rule_id}')

        decrypted_rule_id = int(decrypt(rule_id))
        result = crud.deactivate_rule(db, decrypted_rule_id)
        result.id = decrypted_rule_id

        logger.info(f'deactivate rule {rule_id} success')
    except NoResultFound:
        logger.info(f'deactivate rule {rule_id} failed : not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    
    return result