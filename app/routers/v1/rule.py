import logging
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Union, List

from app.core.connection.postgres import get_session
from app.database.v1.schemas import rule as schema
from app.services.v1 import rule as service

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/v1/rules',
                   responses={500: {'description': 'Internal Server Error'}})

@router.get("/", 
            status_code=status.HTTP_200_OK,
            summary="Get Rules",
            description="Get list of rules",
            response_model=schema.RuleDetailList)
async def get_rules(limit: Union[int, None] = None, session: Session = Depends(get_session)):
    return service.get_rules(session, limit)

@router.get("/{rule_id}", 
            status_code=status.HTTP_200_OK,
            summary="Get Rule Detail",
            description="Create rule detail by id",
            response_model=schema.RuleDetail)
async def get_rule_detail(rule_id: Union[str, None] = None, session: Session = Depends(get_session)):
    return service.get_rule_detail(session, rule_id)

@router.post(path="/", 
            status_code=status.HTTP_201_CREATED,
            summary="Create New Rule",
            description="Create new rule based on given conditions",
            response_model=schema.RuleDetail)
async def create_rule(request: schema.RuleCreate, session: Session = Depends(get_session)):
    return service.create_rule(session, request)

@router.delete("/",
            status_code=status.HTTP_200_OK,
            summary="Delete Rule",
            description="Delete existing rule",
            response_model=schema.RuleDelete)
async def delete_rule(request: schema.RuleDelete, session: Session = Depends(get_session)):
    return service.delete_rule(session, request.id)

@router.put("/", 
            status_code=status.HTTP_200_OK,
            summary="Update Rule",
            description="Update existing rule",
            response_model=schema.RuleDetail)
async def update_rule(request: schema.RuleUpdate, session: Session = Depends(get_session)):
    return service.update_rule(session, request)

@router.post("/activate",
            status_code=status.HTTP_200_OK,
            summary="Activate Rule",
            description="Activate existing rule",
            response_model=schema.RuleDetail)
async def activate_rule(request: schema.RuleState, session: Session = Depends(get_session)):
    return service.activate_rule(session, request.id)

@router.post("/deactivate",
            status_code=status.HTTP_200_OK,
            summary="Deactivate Rule",
            description="Deactivate existing rule",
            response_model=schema.RuleDetail)
async def deactivate_rule(request: schema.RuleState, session: Session = Depends(get_session)):
    return service.deactivate_rule(session, request.id)

@router.get("/edit/history")
async def get_rule_edit_history():
    pass