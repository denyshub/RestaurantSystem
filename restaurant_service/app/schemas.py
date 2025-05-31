from pydantic import validator, AnyHttpUrl
from pydantic import BaseModel, EmailStr, Field, confloat
from typing import Optional
from datetime import datetime


class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    address: str = Field(..., max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    website: Optional[str] = Field(None, max_length=255)
    latitude: Optional[confloat(ge=-90, le=90)] = None
    longitude: Optional[confloat(ge=-180, le=180)] = None

    @validator('website')
    def validate_website(cls, v):
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            v = 'https://' + v
        return v


class RestaurantCreate(RestaurantBase):
    owner_id: Optional[int] = None


class RestaurantUpdate(RestaurantBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class RestaurantInDB(RestaurantBase):
    id: int
    owner_id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RestaurantResponse(RestaurantInDB):
    pass
