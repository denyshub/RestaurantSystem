from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from ..deps import get_current_user_id

router = APIRouter()

@router.post("/", response_model=schemas.RestaurantResponse)
async def create_restaurant(
    restaurant_data: schemas.RestaurantBase,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    restaurant = schemas.RestaurantCreate(
        **restaurant_data.model_dump(),
        owner_id=current_user_id
    )
    return await crud.create_restaurant(db=db, restaurant=restaurant)

@router.get("/my", response_model=List[schemas.RestaurantResponse])
async def read_my_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Отримати всі ресторани поточного користувача"""
    restaurants = await crud.get_restaurants(
        db, 
        skip=skip, 
        limit=limit, 
        owner_id=current_user_id
    )
    return restaurants

@router.get("/{restaurant_id}", response_model=schemas.RestaurantResponse)
async def read_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_restaurant = await crud.get_restaurant(db, restaurant_id=restaurant_id)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@router.get("/", response_model=List[schemas.RestaurantResponse])
async def read_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Отримати всі ресторани"""
    restaurants = await crud.get_restaurants(db, skip=skip, limit=limit)
    return restaurants

@router.put("/{restaurant_id}", response_model=schemas.RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant: schemas.RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    db_restaurant = await crud.update_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        restaurant_update=restaurant,
        current_user_id=current_user_id
    )
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    success = await crud.delete_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        current_user_id=current_user_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}

@router.get("/by-city/{city}", response_model=List[schemas.RestaurantResponse])
async def read_restaurants_by_city(
    city: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    restaurants = await crud.get_restaurants_by_city(db, city=city, skip=skip, limit=limit)
    return restaurants

@router.get("/verified/list", response_model=List[schemas.RestaurantResponse])
async def read_verified_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    restaurants = await crud.get_verified_restaurants(db, skip=skip, limit=limit)
    return restaurants
