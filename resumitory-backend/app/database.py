from sqlmodel import create_engine, Session
from app.config import settings

# Create database engine (Supabase PostgreSQL)
# Format: postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
PROJECT_REF = settings.SUPABASE_URL.replace('https://', '').replace('http://', '').split('.')[0]
DATABASE_URL = f"postgresql://postgres:{settings.DATABASE_PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
