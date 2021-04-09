from fastapi import APIRouter

from db_api.api.api_v1.endpoints import (
    documents,
    entities,
    entity_mentions,
    login,
    ner_evaluations,
    user_ratings,
    users,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    user_ratings.router, prefix="/user_ratings", tags=["user_ratings"]
)
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(
    entity_mentions.router, prefix="/entity_mentions", tags=["entity_mentions"]
)
api_router.include_router(
    ner_evaluations.router, prefix="/ner_evaluations", tags=["ner_evaluations"]
)
