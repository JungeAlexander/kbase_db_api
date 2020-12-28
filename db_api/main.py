from datetime import datetime, timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from mangum import Mangum
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, schemas
from .core import security
from .core.config import settings
from .database import create_session, global_init

global_init()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="kbase document store",
    description="Retrieve, update, and recommend documents, entities and mentions in kbase.",
    # version="v01",
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


# Dependencies
def get_db():
    db = None
    try:
        db = create_session()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = crud.get_user_by_username(db, username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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


@app.post("/entities/", response_model=schemas.Entity)
def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    db_entity = crud.get_entity(db, entity_id=entity.id)
    if db_entity:
        raise HTTPException(
            status_code=400, detail=f"Entity ID {entity.id} already registered."
        )
    return crud.create_entity(db=db, entity=entity)


@app.get("/entities/", response_model=List[schemas.Entity])
def read_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entities = crud.get_entities(db, skip=skip, limit=limit)
    return entities


@app.get("/entities/{entity_id}", response_model=schemas.Entity)
def read_entity(entity_id: str, db: Session = Depends(get_db)):
    db_entity = crud.get_entity(db, entity_id=entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail=f"Entity ID {entity_id} not found")
    return db_entity


@app.put("/entities/{entity_id}", response_model=schemas.Entity)
def update_entity(
    entity_id: str, entity: schemas.EntityUpdate, db: Session = Depends(get_db)
):
    db_entity = crud.get_entity(db, entity_id=entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail=f"Entity ID {entity_id} not found")
    return crud.update_entity(db, entity)


@app.get(
    "/entities/{entity_id}/documents/{document_id}",
    response_model=List[schemas.EntityMention],
)
def get_mentions_by_entity_and_document(
    entity_id: str, document_id: str, db: Session = Depends(get_db)
):
    db_mentions = crud.get_mentions_by_entity_and_document(db, document_id, entity_id)
    if db_mentions is None:
        raise HTTPException(
            status_code=404,
            detail=f"Entity ID {entity_id} is not mentioned in document ID {document_id}.",
        )
    else:
        return db_mentions


@app.post("/entity_mentions/", response_model=schemas.EntityMention)
def create_entity_mention(
    entity_mention: schemas.EntityMentionCreate, db: Session = Depends(get_db)
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


@app.get("/entity_mentions/", response_model=List[schemas.EntityMention])
def read_entity_mentions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    entity_mentions = crud.get_entity_mentions(db, skip=skip, limit=limit)
    return entity_mentions


@app.get("/entity_mentions/{entity_mention_id}", response_model=schemas.EntityMention)
def read_entity_mention(entity_mention_id: int, db: Session = Depends(get_db)):
    db_entity_mention = crud.get_entity_mention(db, entity_mention_id=entity_mention_id)
    if db_entity_mention is None:
        raise HTTPException(
            status_code=404, detail=f"EntityMention ID {entity_mention_id} not found"
        )
    return db_entity_mention


@app.put("/entity_mentions/{entity_mention_id}", response_model=schemas.EntityMention)
def update_entity_mention(
    entity_mention_id: int,
    entity_mention: schemas.EntityMentionUpdate,
    db: Session = Depends(get_db),
):
    db_entity_mention = crud.get_entity_mention(db, entity_mention_id=entity_mention_id)
    if db_entity_mention is None:
        raise HTTPException(
            status_code=404, detail=f"EntityMention ID {entity_mention_id} not found"
        )
    return crud.update_entity_mention(db, entity_mention)


@app.post("/ner_evaluations/", response_model=schemas.NEREvaluation)
def create_ner_evaluation(
    ner_evaluation: schemas.NEREvaluationCreate, db: Session = Depends(get_db)
):
    db_document = crud.get_document(db, document_id=ner_evaluation.document_id)
    if db_document is None:
        raise HTTPException(
            status_code=400,
            detail=f"Document ID {ner_evaluation.document_id} not registered.",
        )
    return crud.create_ner_evaluation(db=db, ner_evaluation=ner_evaluation)


@app.get("/ner_evaluations/", response_model=List[schemas.NEREvaluation])
def read_ner_evaluations(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    ner_evaluations = crud.get_ner_evaluations(db, skip=skip, limit=limit)
    return ner_evaluations


@app.get("/ner_evaluations/{ner_evaluation_id}", response_model=schemas.NEREvaluation)
def read_ner_evaluation(ner_evaluation_id: int, db: Session = Depends(get_db)):
    db_ner_evaluation = crud.get_ner_evaluation(db, ner_evaluation_id=ner_evaluation_id)
    if db_ner_evaluation is None:
        raise HTTPException(
            status_code=404, detail=f"NEREvaluation ID {ner_evaluation_id} not found"
        )
    return db_ner_evaluation


@app.put("/ner_evaluations/{ner_evaluation_id}", response_model=schemas.NEREvaluation)
def update_ner_evaluation(
    ner_evaluation_id: int,
    ner_evaluation: schemas.NEREvaluationUpdate,
    db: Session = Depends(get_db),
):
    db_ner_evaluation = crud.get_ner_evaluation(db, ner_evaluation_id=ner_evaluation_id)
    if db_ner_evaluation is None:
        raise HTTPException(
            status_code=404, detail=f"NEREvaluation ID {ner_evaluation_id} not found"
        )
    return crud.update_ner_evaluation(db, ner_evaluation)


handler = Mangum(app, enable_lifespan=False)
