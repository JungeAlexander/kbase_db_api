from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(deps.get_current_active_user)):
    return current_user


@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered."
        )
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return crud.update_user(db, user)


@router.get("/{user_id}/user_ratings/{document_id}", response_model=schemas.UserRating)
def get_rating_for_user(
    user_id: int,
    document_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_rating = crud.get_user_rating_by_document_and_user(db, document_id, user_id)
    if db_rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} has no rating for document ID {document_id}.",
        )
    return db_rating


@router.put("/{user_id}/user_ratings/{document_id}", response_model=schemas.UserRating)
def update_rating_for_user(
    user_id: int,
    document_id: str,
    user_rating: schemas.UserRatingUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_rating = crud.get_user_rating_by_document_and_user(db, document_id, user_id)
    if db_rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} has no rating for document ID {document_id}.",
        )
    new_user_rating = schemas.UserRating(
        id=db_rating.id,
        user_id=user_id,
        document_id=document_id,
        value=user_rating.value,
        modified_date=datetime.now(),
    )
    return crud.update_user_rating(db, new_user_rating)
