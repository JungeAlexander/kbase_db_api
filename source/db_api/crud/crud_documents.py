from datetime import date
from typing import Iterable

from sqlalchemy.orm import Session

from db_api import models, schemas


def get_document(db: Session, document_id: str) -> models.Document:
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_documents_by_publication_date(
    db: Session, document_date: date
) -> Iterable[models.Document]:
    return (
        db.query(models.Document)
        .filter(models.Document.publication_date == document_date)
        .all()
    )


def get_documents(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.Document]:
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_document_ids(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document.id).offset(skip).limit(limit).all()


def search_document_summary(
    db: Session, query: str = "query"
) -> Iterable[models.Document]:
    search = "%{}%".format(query)
    return (
        db.query(models.Document).filter(models.Document.summary.ilike(search)).all()  # type: ignore
    )


def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(db: Session, document: schemas.DocumentUpdate) -> models.Document:
    # TODO does not seem to update modified_date
    new_document = models.Document(**document.dict())
    old_document = get_document(db, new_document.id)
    db.delete(old_document)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document
