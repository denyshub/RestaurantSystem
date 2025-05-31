from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.USER_SERVICE_URL}/auth/token/")

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_PUBLIC_KEY, 
            algorithms=[settings.ALGORITHM],
            audience="restaurant_service"
        )
        
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        print(user_id)
        return user_id
    except JWTError:
        raise credentials_exception
