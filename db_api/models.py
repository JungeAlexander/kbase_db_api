from datetime import date, datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .database import SqlAlchemyBase


class Document(SqlAlchemyBase):  # type: ignore
    __tablename__ = "documents"

    id: str = sa.Column(sa.String, primary_key=True, index=True)
    version: str = sa.Column(sa.String)
    source: str = sa.Column(sa.String)
    journal: str = sa.Column(sa.String)
    document_type: str = sa.Column(sa.String)
    title: str = sa.Column(sa.String)
    publication_date: date = sa.Column(sa.Date, index=True)
    update_date: date = sa.Column(sa.Date, index=True)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    urls: str = sa.Column(ARRAY(sa.String, dimensions=1))
    pmid: int = sa.Column(sa.Integer)
    arxiv_id: str = sa.Column(sa.String)
    license: str = sa.Column(sa.String)
    doi: str = sa.Column(sa.String)
    summary: str = sa.Column(sa.String)
    full_text: str = sa.Column(sa.String)
    authors: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    affiliations: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    language: str = sa.Column(sa.String)
    keywords: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    in_citations: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    out_citations: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    tags: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    other_ids: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))

    ratings = relationship("UserRating", back_populates="rated_document")
    entities = relationship("EntityMention", back_populates="document")


class User(SqlAlchemyBase):  # type: ignore
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    name = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String)
    created_date = sa.Column(sa.DateTime, default=datetime.now, index=True)
    last_login = sa.Column(sa.DateTime, default=datetime.now, index=True)
    is_active = sa.Column(sa.Boolean, default=True)

    ratings = relationship("UserRating", back_populates="rated_by")


class UserRating(SqlAlchemyBase):  # type: ignore
    __tablename__ = "user_ratings"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    document_id = sa.Column(
        sa.String, sa.ForeignKey("documents.id"), nullable=False, index=True
    )
    value = sa.Column(sa.Float, nullable=False)
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True
    )
    modified_date = sa.Column(sa.DateTime, default=datetime.now, index=True)

    rated_by = relationship("User", back_populates="ratings")
    rated_document = relationship("Document", back_populates="ratings")


class Entity(SqlAlchemyBase):  # type: ignore
    __tablename__ = "entities"
    id: str = sa.Column(sa.String, primary_key=True, index=True)
    preferred_name: str = sa.Column(sa.String, nullable=False, index=True)
    entity_type: str = sa.Column(sa.String)
    synonyms: List[str] = sa.Column(ARRAY(sa.String, dimensions=1))
    source: str = sa.Column(sa.String)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    mentions = relationship("EntityMention", back_populates="entity")


class EntityMention(SqlAlchemyBase):  # type: ignore
    __tablename__ = "entity_mentions"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    document_id = sa.Column(
        sa.String, sa.ForeignKey("documents.id"), nullable=False, index=True
    )
    entity_id = sa.Column(
        sa.String, sa.ForeignKey("entities.id"), nullable=False, index=True
    )
    text: str = sa.Column(sa.String)
    document_section: str = sa.Column(sa.String)
    start_char: int = sa.Column(sa.Integer)
    end_char: int = sa.Column(sa.Integer)
    start_token: int = sa.Column(sa.Integer)
    end_token: int = sa.Column(sa.Integer)
    modified_date: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    document = relationship("Document", back_populates="entities")
    entity = relationship("Entity", back_populates="mentions")
