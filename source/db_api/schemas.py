from datetime import date, datetime
from enum import Enum
from typing import Dict, List

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


class DocumentSection(str, Enum):
    title = "Title"  # type: ignore
    summary = "Summary"
    full_text = "Full text"


class EntityMentionBase(BaseModel):
    document_id: str
    entity_id: str
    text: str
    document_section: DocumentSection
    start_char: int
    end_char: int
    start_token: int
    end_token: int
    source: str


class EntityMentionCreate(EntityMentionBase):
    pass


class EntityMentionUpdate(EntityMentionBase):
    pass


class EntityMention(EntityMentionBase):
    id: int
    modified_date: datetime

    class Config:
        orm_mode = True


class NEREvaluationBase(BaseModel):
    document_id: str
    document_section: DocumentSection
    ner_source: str
    annotation_source: str
    tp: int
    tn: int
    fp: int
    fn: int
    precision: float
    recall: float
    fscore: float


class NEREvaluationCreate(NEREvaluationBase):
    pass


class NEREvaluationUpdate(NEREvaluationBase):
    pass


class NEREvaluation(NEREvaluationBase):
    id: int
    modified_date: datetime

    class Config:
        orm_mode = True


class DocumentType(str, Enum):
    scientific_article = "Scientific article"
    podcast_episode = "Podcast episode"


class DocumentSubType(str, Enum):
    not_specified = "not specified"
    preprint = "preprint"
    postprint = "postprint"
    proceeding = "proceeding"


class TextFormat(str, Enum):
    html = "HTML"
    plain = "Plain text"
    markdown = "Markdown"


class Language(str, Enum):
    english = "English"
    german = "German"
    danish = "Danish"
    na = "NA"


class DocumentBase(BaseModel):
    id: str
    version: str
    source: str
    title: str
    document_type: DocumentType
    publication_date: date
    update_date: date
    urls: List[str]
    summary: str = ""
    raw_text: str = ""
    raw_text_format: TextFormat = TextFormat.plain
    parsed_text: str = ""
    document_subtype: DocumentSubType = DocumentSubType.not_specified
    authors: List[str] = []
    language: Language = Language.na
    keywords: List[str] = []
    tags: List[str] = []
    extra: Dict = {}
    # TODO move to extra
    # Podcast:
    # episode_number : int
    # duration_in_seconds: int
    #
    # Article:
    # journal: str
    # pmid: int = -1
    # license: str = ""
    # doi: str = ""
    # arxiv_id: str = ""
    # in_citations: List[str] = []
    # out_citations: List[str] = []
    # other_ids: List[str] = []


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class Document(DocumentBase):
    modified_date: datetime
    ratings: List[UserRating] = []
    entities: List[EntityMention] = []
    ner_evaluations: List[NEREvaluation] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_superuser: bool = False


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
