from datetime import date
from typing import Iterable, Set, Tuple

from sqlalchemy.orm import Session

from . import models, schemas
from .core import security


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


def search_document_sumary(
    db: Session, query: str = "query"
) -> Iterable[models.Document]:
    search = "%{}%".format(query)
    documents = (
        db.query(models.Document).filter(models.Document.summary.ilike(search)).all()  # type: ignore
    )
    return documents


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


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=hashed_password
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


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Iterable[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


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


def get_mentions_by_entity_and_document(
    db: Session, document_id: str, entity_id: str
) -> Iterable[models.EntityMention]:
    return (
        db.query(models.EntityMention)
        .filter(
            (models.EntityMention.document_id == document_id)
            & (models.EntityMention.entity_id == entity_id)
        )
        .all()
    )


def get_user_ratings(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.UserRating]:
    return db.query(models.UserRating).offset(skip).limit(limit).all()


def create_entity(db: Session, entity: schemas.EntityCreate) -> models.Entity:
    db_entity = models.Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_entity(db: Session, entity_id: str) -> models.Entity:
    return db.query(models.Entity).filter(models.Entity.id == entity_id).first()


def get_entities(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.Entity]:
    return db.query(models.Entity).offset(skip).limit(limit).all()


def update_entity(db: Session, entity: schemas.EntityUpdate) -> models.Entity:
    new_entity = models.Entity(**entity.dict())
    old_entity = get_entity(db, new_entity.id)
    db.delete(old_entity)
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return new_entity


def create_entity_mention(
    db: Session, entity_mention: schemas.EntityMentionCreate
) -> models.EntityMention:
    db_entity_mention = models.EntityMention(**entity_mention.dict())
    db.add(db_entity_mention)
    db.commit()
    db.refresh(db_entity_mention)
    return db_entity_mention


def get_entity_mention(db: Session, entity_mention_id: int) -> models.EntityMention:
    return (
        db.query(models.EntityMention)
        .filter(models.EntityMention.id == entity_mention_id)
        .first()
    )


def get_entity_mentions(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.EntityMention]:
    return db.query(models.EntityMention).offset(skip).limit(limit).all()


def update_entity_mention(
    db: Session, entity_mention: schemas.EntityMentionUpdate
) -> models.EntityMention:
    new_entity_mention = models.EntityMention(**entity_mention.dict())
    old_entity_mention = get_entity_mention(db, new_entity_mention.id)
    db.delete(old_entity_mention)
    db.add(new_entity_mention)
    db.commit()
    db.refresh(new_entity_mention)
    return new_entity_mention


def precision_recall_fscore(
    predicted: Set, gold: Set, beta: float = 1.0
) -> Tuple[float, float, float, int, int, int]:
    tp = len(predicted.intersection(gold))
    fp = len(predicted - gold)
    fn = len(gold - predicted)
    precision = tp / (tp + fp + 1e-100)
    recall = tp / (tp + fn + 1e-100)
    fscore = (1 + beta ** 2) * (
        (precision * recall) / (((beta ** 2) * precision) + recall + 1e-100)
    )
    return precision, recall, fscore, tp, fp, fn


def create_ner_evaluation(
    db: Session, ner_evaluation: schemas.NEREvaluationCreate
) -> models.NEREvaluation:
    db_ner_evaluation = models.NEREvaluation(**ner_evaluation.dict())
    db.add(db_ner_evaluation)
    db.commit()
    db.refresh(db_ner_evaluation)
    return db_ner_evaluation


def get_ner_evaluation(db: Session, ner_evaluation_id: int) -> models.NEREvaluation:
    return (
        db.query(models.NEREvaluation)
        .filter(models.NEREvaluation.id == ner_evaluation_id)
        .first()
    )


def get_ner_evaluations(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.NEREvaluation]:
    return db.query(models.NEREvaluation).offset(skip).limit(limit).all()


def update_ner_evaluation(
    db: Session, ner_evaluation: schemas.NEREvaluationUpdate
) -> models.NEREvaluation:
    new_ner_evaluation = models.NEREvaluation(**ner_evaluation.dict())
    old_ner_evaluation = get_ner_evaluation(db, ner_evaluation.id)
    db.delete(old_ner_evaluation)
    db.add(new_ner_evaluation)
    db.commit()
    db.refresh(new_ner_evaluation)
    return new_ner_evaluation
