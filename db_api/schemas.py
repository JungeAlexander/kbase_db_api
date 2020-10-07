from datetime import date, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr


class UserRatingBase(BaseModel):
    value: float


class UserRatingCreate(UserRatingBase):
    article_id: str
    user_id: int


class UserRatingUpdate(UserRatingBase):
    pass


class UserRating(UserRatingCreate):
    id: int
    modified_date: datetime

    class Config:
        orm_mode = True


class ArticleType(str, Enum):
    preprint = "preprint"
    postprint = "postprint"
    proceeding = "proceeding"


class ArticleBase(BaseModel):
    id: str
    version: str
    source: str
    journal: str
    article_type: ArticleType
    title: str
    publication_date: date
    update_date: date
    urls: List[str]
    pmid: int = -1
    license: str = ""
    doi: str = ""
    summary: str = ""
    full_text: str = ""
    authors: List[str] = []
    affiliations: List[str] = []
    language: str = ""
    keywords: List[str] = []
    in_citations: List[str] = []
    out_citations: List[str] = []
    tags: List[str] = []
    other_ids: List[str] = []


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class Article(ArticleBase):
    modified_date: datetime
    ratings: List[UserRating] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_date: datetime
    last_login: datetime
    is_active: bool
    ratings: List[UserRating] = []

    class Config:
        orm_mode = True
