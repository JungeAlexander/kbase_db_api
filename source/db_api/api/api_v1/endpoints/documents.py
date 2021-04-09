from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Document)
def create_document(
    document: schemas.DocumentCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document_id = document.id
    db_document = crud.get_document(db, document_id=document_id)
    if db_document:
        raise HTTPException(
            status_code=400, detail=f"Document with id {document_id} already registered"
        )
    return crud.create_document(db=db, document=document)


@router.get("/", response_model=List[schemas.Document])
def read_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents


@router.put("/{document_id}", response_model=schemas.Document)
def update_document(
    document_id: str,
    document: schemas.DocumentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_document = crud.get_document(db, document_id=document_id)
    if not db_document:
        raise HTTPException(
            status_code=400, detail=f"Document with id {document_id} does not exist"
        )
    return crud.update_document(db=db, document=document)


@router.get("/{document_id}", response_model=schemas.Document)
def read_document(
    document_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document


@router.get("/ids", response_model=List[schemas.ID])
def read_document_ids(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    documents = crud.get_document_ids(db, skip=skip, limit=limit)
    return documents


@router.get("/search_summary", response_model=List[schemas.Document])
def search_document_summary(
    query: str = "query",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    documents = crud.search_document_summary(db, query=query)
    return documents
