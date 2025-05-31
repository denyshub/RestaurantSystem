from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # JWT Public key for verifying tokens from user service
    JWT_PUBLIC_KEY: str
    USER_SERVICE_URL: str = "http://user_service:8000"

    class Config:
        env_file = ".env"

settings = Settings()
