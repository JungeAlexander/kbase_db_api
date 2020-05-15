from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SqlAlchemyBase = declarative_base()

SessionLocal = None


def global_init():
    global SessionLocal

    if SessionLocal:
        return

    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import models

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
