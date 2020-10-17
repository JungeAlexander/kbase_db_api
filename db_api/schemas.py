from datetime import date, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr


class UserRatingBase(BaseModel):
    value: float


class UserRatingCreate(UserRatingBase):
    document_id: str
    user_id: int


class UserRatingUpdate(UserRatingBase):
    pass


class UserRating(UserRatingCreate):
    id: int
    modified_date: datetime

    class Config:
        orm_mode = True


class DocumentType(str, Enum):
    preprint = "preprint"
    postprint = "postprint"
    proceeding = "proceeding"


class DocumentBase(BaseModel):
    id: str
    version: str
    source: str
    journal: str
    document_type: DocumentType
    title: str
    publication_date: date
    update_date: date
    urls: List[str]
    pmid: int = -1
    license: str = ""
    doi: str = ""
    arxiv_id: str = ""
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


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class Document(DocumentBase):
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


class DocumentSection(str, Enum):
    title = "title"
    summary = "summary"
    full_text = "full_text"


class EntityMentionBase(BaseModel):
    document_id: str
    entity_id: str
    text: str
    document_section: DocumentSection
    start_char: int
    end_char: int
    start_token: int
    end_token: int


class EntityMentionCreate(EntityMentionBase):
    pass


class EntityMentionUpdate(EntityMentionBase):
    pass


class EntityMention(EntityMentionBase):
    id: int
    modified_date: datetime

    class Config:
        orm_mode = True


class EntityBase(BaseModel):
    id: str
    preferred_name: str
    entity_type: str
    synonyms: List[str]
    source: str


class EntityCreate(EntityBase):
    pass


class EntityUpdate(EntityBase):
    pass


class Entity(EntityBase):
    modified_date: datetime
    mentions: List[EntityMention]

    class Config:
        orm_mode = True
