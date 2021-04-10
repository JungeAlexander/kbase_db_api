from typing import Iterable

from sqlalchemy.orm import Session

from db_api import models, schemas


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
