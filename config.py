import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Use SQLite for simplicity (no Docker required)
    database_url: str = "sqlite:///./candy_patterns.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    json_input_path: str = "/Users/victoria.serrano/Downloads/LIVE-collection-levels (12)"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
