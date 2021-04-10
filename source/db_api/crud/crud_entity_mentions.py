from typing import Iterable

from sqlalchemy.orm import Session

from db_api import models, schemas


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
