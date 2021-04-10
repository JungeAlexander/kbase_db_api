from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.NEREvaluation)
def create_ner_evaluation(
    ner_evaluation: schemas.NEREvaluationCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_document = crud.get_document(db, document_id=ner_evaluation.document_id)
    if db_document is None:
        raise HTTPException(
            status_code=400,
            detail=f"Document ID {ner_evaluation.document_id} not registered.",
        )
    return crud.create_ner_evaluation(db=db, ner_evaluation=ner_evaluation)


@router.get("/", response_model=List[schemas.NEREvaluation])
def read_ner_evaluations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.get_ner_evaluations(db, skip=skip, limit=limit)


@router.get("/{ner_evaluation_id}", response_model=schemas.NEREvaluation)
def read_ner_evaluation(
    ner_evaluation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_ner_evaluation = crud.get_ner_evaluation(db, ner_evaluation_id=ner_evaluation_id)
    if db_ner_evaluation is None:
        raise HTTPException(
            status_code=404, detail=f"NEREvaluation ID {ner_evaluation_id} not found"
        )
    return db_ner_evaluation


@router.put("/{ner_evaluation_id}", response_model=schemas.NEREvaluation)
def update_ner_evaluation(
    ner_evaluation_id: int,
    ner_evaluation: schemas.NEREvaluationUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_ner_evaluation = crud.get_ner_evaluation(db, ner_evaluation_id=ner_evaluation_id)
    if db_ner_evaluation is None:
        raise HTTPException(
            status_code=404, detail=f"NEREvaluation ID {ner_evaluation_id} not found"
        )
    return crud.update_ner_evaluation(db, ner_evaluation)
