from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from . import models, schemas
from typing import List, Optional
from fastapi import HTTPException

async def create_restaurant(db: AsyncSession, restaurant: schemas.RestaurantCreate) -> models.Restaurant:
    print(restaurant)
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

async def get_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[models.Restaurant]:
    query = select(models.Restaurant).where(models.Restaurant.id == restaurant_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None
) -> List[models.Restaurant]:
    query = select(models.Restaurant)
    if owner_id is not None:
        query = query.where(models.Restaurant.owner_id == owner_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_restaurant(
    db: AsyncSession,
    restaurant_id: int,
    restaurant_update: schemas.RestaurantUpdate,
    current_user_id: int
) -> Optional[models.Restaurant]:
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if restaurant.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions to update this restaurant")

    update_data = restaurant_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")

    if 'owner_id' in update_data:
        raise HTTPException(status_code=400, detail="Cannot change restaurant owner")

    query = update(models.Restaurant).where(
        models.Restaurant.id == restaurant_id
    ).values(update_data).returning(models.Restaurant)
    
    result = await db.execute(query)
    await db.commit()
    
    return result.scalar_one_or_none()

async def delete_restaurant(
    db: AsyncSession,
    restaurant_id: int,
    current_user_id: int
) -> bool:
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if restaurant.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete this restaurant")

    query = delete(models.Restaurant).where(
        models.Restaurant.id == restaurant_id,
        models.Restaurant.owner_id == current_user_id
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0

async def get_restaurants_by_city(
    db: AsyncSession,
    city: str,
    skip: int = 0,
    limit: int = 100
) -> List[models.Restaurant]:
    query = select(models.Restaurant).where(
        models.Restaurant.city == city
    ).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_verified_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[models.Restaurant]:
    query = select(models.Restaurant).where(
        models.Restaurant.is_verified == True
    ).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
