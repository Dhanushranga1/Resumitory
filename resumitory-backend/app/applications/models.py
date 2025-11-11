from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class StatusEnum(str, Enum):
    """Application status enum."""
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    archived = "archived"


class ApplicationBase(SQLModel):
    """Base model for Application with common fields."""
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job role/title")
    date_applied: date = Field(..., description="Date when application was submitted")
    status: StatusEnum = Field(default=StatusEnum.applied, description="Current application status")
    notes: Optional[str] = Field(default=None, description="Optional notes about the application")
    resume_id: Optional[UUID] = Field(default=None, foreign_key="resumes.id", description="Linked resume ID")
    follow_up_date: Optional[date] = Field(default=None, description="Date to follow up on application")


class Application(ApplicationBase, table=True):
    """Application database model with full schema."""
    __tablename__ = "applications"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(..., foreign_key="auth.users.id", index=True)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ApplicationCreate(ApplicationBase):
    """Schema for creating a new application."""
    pass


class ApplicationUpdate(SQLModel):
    """Schema for updating an application (all fields optional)."""
    company: Optional[str] = None
    role: Optional[str] = None
    date_applied: Optional[date] = None
    status: Optional[StatusEnum] = None
    notes: Optional[str] = None
    resume_id: Optional[UUID] = None
    follow_up_date: Optional[date] = None


class ApplicationResponse(ApplicationBase):
    """Schema for application API responses."""
    id: UUID
    user_id: UUID
    last_updated: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationWithResume(ApplicationResponse):
    """Extended response that includes resume name."""
    resume_name: Optional[str] = None
    
    class Config:
        from_attributes = True
