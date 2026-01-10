from pydantic import BaseSettings
 
class Settings(BaseSettings):
    #Configurações gerais da aplicação
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    API_V1_STR: str = "/api/v1"

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    PROJECT_NAME: str = "Cursos API - FastAPI SQL Model"

    class Config():
        env_file = ".env"
        case_sensitive = True

settings: Settings = Settings()