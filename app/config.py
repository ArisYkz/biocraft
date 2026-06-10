from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Biocraft"
    SECRET_KEY: str = "CHANGE-ME-use-env-file-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/biocraft_dev"

    class Config:
        env_file = ".env"


settings = Settings()
