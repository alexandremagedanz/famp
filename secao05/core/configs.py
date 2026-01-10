from pydantic import BaseSettings
 
class Settings(BaseSettings):
    #Configurações gerais da aplicação
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:Alex01-lo@localhost:5432/faculdade"
    PROJECT_NAME: str = "Cursos API - FastAPI SQL Model"

    class Config():
        case_sensitive = True

settings: Settings = Settings()