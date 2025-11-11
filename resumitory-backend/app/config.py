from pydantic_settings import BaseSettings
from pathlib import Path

# Get the base directory (resumitory-backend/)
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""
    
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    DATABASE_PASSWORD: str
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        case_sensitive = True


settings = Settings()
