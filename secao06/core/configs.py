from typing import List
from pydantic import BaseSettings, Field
from sqlalchemy.ext.declarative import declarative_base
 
class Settings(BaseSettings):
    #Configurações gerais da aplicação
    DB_USER: str = Field(default=None, env="DB_USER")
    DB_PASSWORD: str = Field(default=None, env="DB_PASSWORD")
    DB_HOST: str = Field(default=None, env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default=None, env="DB_NAME")
    API_JWT_SECRET: str = Field(default=None, env="API_JWT_SECRET")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cursos API - FastAPI SQL Model"
    DBBaseModel = declarative_base()

    """
    Gerendo um Secret Key para JWT - rodar no python shell
    import secrets
    secrets.token_urlsafe(32)
    """

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def JWT_SECRET(self) -> str:
        return self.API_JWT_SECRET

    class Config(BaseSettings.Config):
        env_file = ".env"
        case_sensitive = True

settings: Settings = Settings()