from dotenv import load_dotenv
from pydantic import Field
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    database_url: str = Field(..., alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()

