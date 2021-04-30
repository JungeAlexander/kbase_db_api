from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.core.config import settings
from db_api.database import create_async_session, create_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")


def get_db() -> Session:
    db = None
    try:
        db = create_session()
        yield db
    finally:
        db.close()


async def get_db_async() -> AsyncSession:
    db = None
    try:
        db = create_async_session()
        yield db
    finally:
        await db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_async)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = await crud.get_user_by_username(db, username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough privileges")
    return current_user
