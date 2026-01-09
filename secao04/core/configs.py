from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    #Configurações gerais da aplicação
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:Alex01-lo@localhost:5432/faculdade"
    DBBaseModel = declarative_base()
    PROJECT_NAME: str = "Cursos API - FastAPI SQL Alchemy"

    class Config():
        case_sensitive = True

settings = Settings()

