import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/v1/rules',
                   tags=["rules"],
                   responses={500: {'description': 'Internal Server Error'}})

@router.get("/")
async def get_rules():
    pass

@router.post("/")
async def add_rules():
    pass

@router.delete("/")
async def delete_rules():
    pass

@router.put("/")
async def edit_rules():
    pass