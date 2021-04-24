import os

import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from db_api.api.api_v1.api import api_router
from db_api.core.config import settings

if os.environ.get("AWS_EXECUTION_ENV"):
    openapi_prefix = f"/{settings.DBAPI_STAGE}"
else:
    openapi_prefix = ""

app = FastAPI(
    title="kbase document store",
    description="Retrieve, update, and recommend documents, entities and mentions in kbase.",
    openapi_prefix=openapi_prefix,
)

origins = [
    "http://localhost:8080",
    "http://localhost:8088",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


handler = Mangum(app, lifespan="off")


def main():
    configure()
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)


def configure():
    configure_routes()


def configure_routes():
    app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    main()
else:
    configure()
