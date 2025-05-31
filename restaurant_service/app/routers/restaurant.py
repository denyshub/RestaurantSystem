from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas

router = APIRouter()

@router.get("/")
async def get_restaurants(db: AsyncSession = Depends(get_db)):
    return {"message": "Restaurant endpoint is working!"}
