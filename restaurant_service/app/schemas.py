from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from datetime import datetime


class RestaurantBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    address: str = Field(..., max_length=255)
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False


class RestaurantCreate(RestaurantBase):
    owner_id: int  # обов’язково вказати при створенні


class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class RestaurantInDBBase(RestaurantBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Restaurant(RestaurantInDBBase):
    pass
