from typing import Iterable

from sqlalchemy.orm import Session

from db_api import models, schemas


def create_user_rating(
    db: Session, user_rating: schemas.UserRatingCreate
) -> models.UserRating:
    db_user_rating = models.UserRating(**user_rating.dict())
    db.add(db_user_rating)
    db.commit()
    db.refresh(db_user_rating)
    return db_user_rating


def update_user_rating(
    db: Session, user_rating: schemas.UserRating
) -> models.UserRating:
    old_rating = get_user_rating(db, user_rating.id)
    new_rating = models.UserRating(**user_rating.dict())
    db.delete(old_rating)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


def get_user_rating(db: Session, user_rating_id: int) -> models.UserRating:
    return (
        db.query(models.UserRating)
        .filter(models.UserRating.id == user_rating_id)
        .first()
    )


def get_user_ratings_by_user(db: Session, user_id: int) -> Iterable[models.UserRating]:
    return (
        db.query(models.UserRating).filter(models.UserRating.user_id == user_id).all()
    )


def get_user_ratings_by_document(
    db: Session, document_id: str
) -> Iterable[models.UserRating]:
    return (
        db.query(models.UserRating)
        .filter(models.UserRating.document_id == document_id)
        .all()
    )


def get_user_rating_by_document_and_user(
    db: Session, document_id: str, user_id: int
) -> models.UserRating:
    return (
        db.query(models.UserRating)
        .filter(
            (models.UserRating.document_id == document_id)
            & (models.UserRating.user_id == user_id)
        )
        .first()
    )


def get_user_ratings(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.UserRating]:
    return db.query(models.UserRating).offset(skip).limit(limit).all()
