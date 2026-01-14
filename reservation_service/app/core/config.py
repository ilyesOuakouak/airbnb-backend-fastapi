import os
from pydantic_settings import BaseSettings

def detect_env_file():
    if os.path.exists("/.dockerenv"):
        return ".env.docker"
    return ".env.local"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "supersecretkey"
    REDIS_URL: str = "redis://redis:6379"

    class Config:
        env_file = detect_env_file()


settings = Settings()