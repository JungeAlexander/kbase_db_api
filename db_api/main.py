from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, schemas
from .database import create_session, global_init

global_init()

app = FastAPI(
    title="kbase document store",
    description="Retrieve, update, and recommend documents in kbase.",
    # version="v1",
    # openapi_prefix="/prod",
)

origins = [
    "http://localhost:8080",
    "http://localhost:8088",
    "http://app-kbase-ajs-aws.s3-website-eu-west-1.amazonaws.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = None
    try:
        db = create_session()
        yield db
    finally:
        db.close()


@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    document_id = document.id
    db_document = crud.get_document(db, document_id=document_id)
    if db_document:
        raise HTTPException(
            status_code=400, detail=f"Document with id {document_id} already registered"
        )
    return crud.create_document(db=db, document=document)


@app.put("/documents/{document_id}", response_model=schemas.Document)
def update_document(
    document_id: str, document: schemas.DocumentUpdate, db: Session = Depends(get_db)
):
    db_document = crud.get_document(db, document_id=document_id)
    if not db_document:
        raise HTTPException(
            status_code=400, detail=f"Document with id {document_id} does not exist"
        )
    return crud.update_document(db=db, document=document)


@app.get("/documents/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents


@app.get("/documents/search_summary", response_model=List[schemas.Document])
def search_document_sumary(query: str = "query", db: Session = Depends(get_db)):
    documents = crud.search_document_sumary(db, query=query)
    return documents


@app.get("/documents/{document_id}", response_model=schemas.Document)
def read_document(document_id: str, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email {user.email} already registered."
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return crud.update_user(db, user)


@app.get(
    "/users/{user_id}/user_ratings/{document_id}", response_model=schemas.UserRating
)
def get_rating_for_user(user_id: int, document_id: str, db: Session = Depends(get_db)):
    db_rating = crud.get_user_rating_by_document_and_user(db, document_id, user_id)
    if db_rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} has no rating for document ID {document_id}.",
        )
    return db_rating


@app.put(
    "/users/{user_id}/user_ratings/{document_id}", response_model=schemas.UserRating
)
def update_rating_for_user(
    user_id: int,
    document_id: str,
    user_rating: schemas.UserRatingUpdate,
    db: Session = Depends(get_db),
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


@app.get("/user_ratings/", response_model=List[schemas.UserRating])
def read_user_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_ratings = crud.get_user_ratings(db, skip=skip, limit=limit)
    return user_ratings


@app.post("/user_ratings/", response_model=schemas.UserRating)
def create_rating_for_user(
    user_rating: schemas.UserRatingCreate, db: Session = Depends(get_db)
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


handler = Mangum(app, enable_lifespan=False)
