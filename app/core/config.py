import os
from pydantic_settings import BaseSettings

def detect_env_file():
    if os.path.exists("/.dockerenv"):
        return ".env.docker"
    return ".env.local"

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"
    RESERVATION_SERVICE_URL: str = "http://reservation_api:8001"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = detect_env_file()

settings = Settings()