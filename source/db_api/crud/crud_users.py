from typing import Iterable, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db_api import models, schemas
from db_api.core import security


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: schemas.UserUpdate) -> models.User:
    old_user = await get_user_by_email(db, user.email)
    new_user = models.User(id=old_user.id, **user.dict())
    await db.delete(old_user)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    query = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    query = select(models.User).filter(models.User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_username(
    db: AsyncSession, username: str
) -> Optional[models.User]:
    query = select(models.User).filter(models.User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Iterable[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> Optional[models.User]:
    user = await get_user_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user
