from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db_api import crud, models, schemas
from db_api.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserRating])
def read_user_ratings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    user_ratings = crud.get_user_ratings(db, skip=skip, limit=limit)
    return user_ratings


@router.post("/", response_model=schemas.UserRating)
def create_rating_for_user(
    user_rating: schemas.UserRatingCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    document_id = user_rating.document_id
    user_id = user_rating.user_id
    db_user_rating = crud.get_user_rating_by_document_and_user(db, document_id, user_id)
    if db_user_rating:
        raise HTTPException(
            status_code=400,
            detail=f"Rating for document id {document_id} by user id {user_id} already registered",
        )
    return crud.create_user_rating(db=db, user_rating=user_rating)
