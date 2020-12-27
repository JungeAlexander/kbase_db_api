import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: str
    DBNAME: str
    DBUSER: str
    DBPASSWORD: str

    SQLALCHEMY_DATABASE_URL = f"postgresql://{DBUSER}:{DBPASSWORD}@{HOST}:{PORT}/{DBNAME}"

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "aws.env"))


settings = Settings()
