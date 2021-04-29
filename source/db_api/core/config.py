import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class _Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    HOST: str
    PSQL_PORT: str
    DBNAME: str
    DBUSER: str
    DBPASSWORD: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str

    DBAPI_STAGE: str

    TESTING: int = int(os.getenv("TESTING", 0))

    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DBUSER"),
            password=values.get("DBPASSWORD"),
            host=values.get("HOST"),
            path=f"/{values.get('DBNAME') or ''}",
            port=values.get("PSQL_PORT"),
        )

    class Config:
        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "aws.env")
        )


settings = _Settings()
