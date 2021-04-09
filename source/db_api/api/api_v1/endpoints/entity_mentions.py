from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.EntityMention)
def create_entity_mention(
    entity_mention: schemas.EntityMentionCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_document = crud.get_document(db, document_id=entity_mention.document_id)
    if db_document is None:
        raise HTTPException(
            status_code=400,
            detail=f"Document ID {entity_mention.document_id} not registered.",
        )
    db_entity = crud.get_entity(db, entity_id=entity_mention.entity_id)
    if db_entity is None:
        raise HTTPException(
            status_code=400,
            detail=f"Entity ID {entity_mention.entity_id} not registered.",
        )
    return crud.create_entity_mention(db=db, entity_mention=entity_mention)


@router.get("/", response_model=List[schemas.EntityMention])
def read_entity_mentions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    entity_mentions = crud.get_entity_mentions(db, skip=skip, limit=limit)
    return entity_mentions


@router.get("/{entity_mention_id}", response_model=schemas.EntityMention)
def read_entity_mention(
    entity_mention_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_entity_mention = crud.get_entity_mention(db, entity_mention_id=entity_mention_id)
    if db_entity_mention is None:
        raise HTTPException(
            status_code=404, detail=f"EntityMention ID {entity_mention_id} not found"
        )
    return db_entity_mention


@router.put("/{entity_mention_id}", response_model=schemas.EntityMention)
def update_entity_mention(
    entity_mention_id: int,
    entity_mention: schemas.EntityMentionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_entity_mention = crud.get_entity_mention(db, entity_mention_id=entity_mention_id)
    if db_entity_mention is None:
        raise HTTPException(
            status_code=404, detail=f"EntityMention ID {entity_mention_id} not found"
        )
    return crud.update_entity_mention(db, entity_mention)
