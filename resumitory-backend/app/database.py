from sqlmodel import create_engine, Session
from app.config import settings

# Create database engine (Supabase PostgreSQL)
DATABASE_URL = f"postgresql://postgres:{settings.SUPABASE_KEY}@{settings.SUPABASE_URL.replace('https://', '').replace('http://', '')}:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
