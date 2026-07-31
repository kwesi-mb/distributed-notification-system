from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: str

    DATABASE_URL: str

    REDIS_URL: str

    RABBITMQ_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    REDIS_URL: str = "redis://localhost:6379/0"

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()