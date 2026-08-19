"""Configuration settings for Tourismo API"""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_TITLE: str = "Tourismo API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Travel Agency Management System REST API"

    # Database
    DATABASE_URL: str = "sqlite:///./tourismo.db"
    # Example PostgreSQL: "postgresql://user:password@localhost:5432/tourismo"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Features
    DEBUG: bool = True
    TESTING: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
