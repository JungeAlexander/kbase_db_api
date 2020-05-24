from datetime import datetime, date
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, schemas
from .database import create_session, global_init, session_scope

global_init()

app = FastAPI(
    title="kbase article store",
    description="Retrieve, update, and recommend articles in kbase.",
    version="v1",
    openapi_prefix="/prod",
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


@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article_id = article.id
    db_article = crud.get_article(db, article_id=article_id)
    if db_article:
        raise HTTPException(
            status_code=400, detail=f"Article with id {article_id} already registered"
        )
    return crud.create_article(db=db, article=article)


def generate_example_article():
    a = schemas.Article(
        id="ABC",
        version="1",
        source="arxiv",
        journal="arxiv",
        article_type=schemas.ArticleType.preprint,
        title="TEST",
        publication_date=date(2020, 2, 2),
        update_date=date(2020, 2, 2),
        modified_date=datetime(2020, 2, 2, 2),
        link="",
        doid="aefef",
        summary="",
        authors="",
        affiliations="",
        language="",
        keywords="",
        references="",
        ratings=[],
    )
    return a


@app.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: str, article: schemas.ArticleUpdate, db: Session = Depends(get_db)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=400, detail=f"Article with id {article_id} does not exist"
        )
    return crud.update_article(db=db, article=article)


@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles


@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: str, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


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
    "/users/{user_id}/user_ratings/{article_id}", response_model=schemas.UserRating
)
def get_rating_for_user(user_id: int, article_id: str, db: Session = Depends(get_db)):
    db_rating = crud.get_user_rating_by_article_and_user(db, article_id, user_id)
    if db_rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} has no rating for article ID {article_id}.",
        )
    return db_rating


@app.put(
    "/users/{user_id}/user_ratings/{article_id}", response_model=schemas.UserRating
)
def update_rating_for_user(
    user_id: int,
    article_id: str,
    user_rating: schemas.UserRatingUpdate,
    db: Session = Depends(get_db),
):
    db_rating = crud.get_user_rating_by_article_and_user(db, article_id, user_id)
    if db_rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} has no rating for article ID {article_id}.",
        )
    new_user_rating = schemas.UserRating(
        id=db_rating.id,
        user_id=user_id,
        article_id=article_id,
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
    article_id = user_rating.article_id
    user_id = user_rating.user_id
    db_user_rating = crud.get_user_rating_by_article_and_user(db, article_id, user_id)
    if db_user_rating:
        raise HTTPException(
            status_code=400,
            detail=f"Rating for article id {article_id} by user id {user_id} already registered",
        )
    return crud.create_user_rating(db=db, user_rating=user_rating)


handler = Mangum(app, enable_lifespan=False)