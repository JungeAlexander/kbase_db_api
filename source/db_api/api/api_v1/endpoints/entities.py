from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Entity)
def create_entity(
    entity: schemas.EntityCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_entity = crud.get_entity(db, entity_id=entity.id)
    if db_entity:
        raise HTTPException(
            status_code=400, detail=f"Entity ID {entity.id} already registered."
        )
    return crud.create_entity(db=db, entity=entity)


@router.get("/", response_model=List[schemas.Entity])
def read_entities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.get_entities(db, skip=skip, limit=limit)


@router.get("/{entity_id}", response_model=schemas.Entity)
def read_entity(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_entity = crud.get_entity(db, entity_id=entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail=f"Entity ID {entity_id} not found")
    return db_entity


@router.put("/{entity_id}", response_model=schemas.Entity)
def update_entity(
    entity_id: str,
    entity: schemas.EntityUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_entity = crud.get_entity(db, entity_id=entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail=f"Entity ID {entity_id} not found")
    return crud.update_entity(db, entity)


@router.get(
    "/{entity_id}/documents/{document_id}",
    response_model=List[schemas.EntityMention],
)
def get_mentions_by_entity_and_document(
    entity_id: str,
    document_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_mentions = crud.get_mentions_by_entity_and_document(db, document_id, entity_id)
    if db_mentions is None:
        raise HTTPException(
            status_code=404,
            detail=f"Entity ID {entity_id} is not mentioned in document ID {document_id}.",
        )
    else:
        return db_mentions
