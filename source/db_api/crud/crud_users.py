from typing import Iterable, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db_api import models, schemas
from db_api.core import security


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate) -> models.User:
    old_user = get_user_by_email(db, user.email)
    new_user = models.User(id=old_user.id, **user.dict())
    db.delete(old_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


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
