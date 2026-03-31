from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://messenger_user:password@localhost:5432/messenger")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "supersecretkey123456")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()