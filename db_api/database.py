from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .core.config import settings

SqlAlchemyBase = declarative_base()

SessionLocal = None


def setup():
    global SessionLocal

    if SessionLocal:
        return

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import models

    return engine


def global_init():
    engine = setup()
    if engine is None:
        return
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global SessionLocal

    session: Session = SessionLocal()

    session.expire_on_commit = False

    return session


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global SessionLocal

    session: Session = SessionLocal()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
