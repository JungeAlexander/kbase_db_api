import fastapi_chameleon
import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from db_api.api.api_v1.api import api_router
from db_api.core.config import settings

app = FastAPI(
    title="kbase document store",
    description="Retrieve, update, and recommend documents, entities and mentions in kbase.",
    openapi_prefix=f"/{settings.DBAPI_STAGE}",
    openapi_url=f"{settings.DBAPI_STAGE}/{settings.API_V1_STR}/openapi.json",
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


handler = Mangum(app, enable_lifespan=False)


def main():
    configure(dev_mode=True)
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)


def configure(dev_mode: bool):
    configure_templates(dev_mode)
    configure_routes()


def configure_templates(dev_mode: bool):
    fastapi_chameleon.global_init("templates", auto_reload=dev_mode)


def configure_routes():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    main()
else:
    configure(dev_mode=False)
