from contextlib import asynccontextmanager, contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from db_api.core.config import settings

SqlAlchemyBase = declarative_base()

SessionLocal = None

AsyncEngineLocal: Optional[AsyncEngine] = None


def setup():
    global SessionLocal
    global AsyncEngineLocal

    if SessionLocal:
        return

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(bind=engine)

    AsyncEngineLocal = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

    # noinspection PyUnresolvedReferences
    from . import models  # noqa: F401

    return engine


def global_init():
    engine = setup()
    if engine is None:
        return
    # Table creation is handled by alembic
    # SqlAlchemyBase.metadata.create_all(engine)

    from db_api import crud, schemas

    with session_scope() as db:
        user = crud.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not user:
            user_in = schemas.UserCreate(
                username=settings.FIRST_SUPERUSER,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.create_user(db, user=user_in)  # noqa: F841


def create_session() -> Session:
    global SessionLocal

    if SessionLocal is None:
        setup()

    session: Session = SessionLocal()

    session.expire_on_commit = False

    return session


def create_async_session() -> AsyncSession:
    global AsyncEngineLocal

    if AsyncEngineLocal is None:
        setup()

    session: AsyncSession = AsyncSession(AsyncEngineLocal)

    session.sync_session.expire_on_commit = False

    return session


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global SessionLocal

    if SessionLocal is None:
        setup()

    session: Session = SessionLocal()

    try:
        yield session
        session.commit()
    except:  # noqa: E722
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def async_session_scope():
    """Provide a transactional async scope around a series of operations."""
    global AsyncEngineLocal

    if AsyncEngineLocal is None:
        setup()

    session: AsyncSession = AsyncSession(AsyncEngineLocal)

    try:
        yield session
        await session.commit()
    except:  # noqa: E722
        await session.rollback()
        raise
    finally:
        await session.close()
