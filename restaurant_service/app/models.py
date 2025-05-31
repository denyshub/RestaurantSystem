from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from datetime import datetime
from restaurant_service.app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # verified by moderator

    owner_id = Column(Integer, index=True, nullable=False)  # user ID from user_service
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
