from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


class ResumeBase(SQLModel):
    """Base model for Resume with common fields."""
    name: str = Field(..., description="Resume name (e.g., 'SWE Resume v3')")
    notes: Optional[str] = Field(None, description="Optional notes about this resume version")
    pdf_url: str = Field(..., description="Supabase Storage URL for PDF file")
    tex_url: Optional[str] = Field(None, description="Supabase Storage URL for LaTeX .tex file")
    tags: Optional[List[str]] = Field(default=None, description="Tags for categorization")


class Resume(ResumeBase, table=True):
    """Resume database model with full schema."""
    __tablename__ = "resumes"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(..., foreign_key="auth.users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResumeCreate(ResumeBase):
    """Schema for creating a new resume (multipart form data handled separately)."""
    pass


class ResumeUpdate(SQLModel):
    """Schema for updating resume metadata (not files)."""
    name: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class ResumeResponse(ResumeBase):
    """Schema for resume API responses."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
