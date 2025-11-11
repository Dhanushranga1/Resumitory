from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID

from app.database import get_session
from app.auth.dependencies import get_current_user
from app.resumes.models import Resume, ResumeCreate, ResumeUpdate, ResumeResponse
from app.resumes.storage import (
    upload_file,
    delete_file,
    validate_file_size,
    validate_file_type
)

router = APIRouter()


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    name: str = Form(..., description="Resume name"),
    notes: Optional[str] = Form(None, description="Optional notes"),
    tags: Optional[str] = Form(None, description="Comma-separated tags"),
    pdf_file: UploadFile = File(..., description="PDF file (required)"),
    tex_file: Optional[UploadFile] = File(None, description="LaTeX .tex file (optional)"),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Upload a new resume with PDF (required) and optional .tex file.
    
    - **name**: Resume name (e.g., "SWE Resume v3")
    - **notes**: Optional notes about this version
    - **tags**: Comma-separated tags (e.g., "python,backend,senior")
    - **pdf_file**: PDF file (max 5MB)
    - **tex_file**: Optional LaTeX source file (max 1MB)
    """
    # Validate PDF file
    await validate_file_type(pdf_file, ['pdf'])
    await validate_file_size(pdf_file, max_size_mb=5)
    
    # Upload PDF
    pdf_url = await upload_file(pdf_file, user_id, 'pdf')
    
    # Upload .tex if provided
    tex_url = None
    if tex_file:
        await validate_file_type(tex_file, ['tex'])
        await validate_file_size(tex_file, max_size_mb=1)
        tex_url = await upload_file(tex_file, user_id, 'tex')
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else None
    
    # Create resume record
    resume = Resume(
        user_id=UUID(user_id),
        name=name,
        notes=notes,
        pdf_url=pdf_url,
        tex_url=tex_url,
        tags=tag_list
    )
    
    session.add(resume)
    session.commit()
    session.refresh(resume)
    
    return resume


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get all resumes for the authenticated user.
    
    Returns resumes ordered by creation date (newest first).
    """
    statement = select(Resume).where(
        Resume.user_id == UUID(user_id)
    ).order_by(Resume.created_at.desc())
    
    resumes = session.exec(statement).all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get a specific resume by ID.
    
    Returns 404 if resume doesn't exist or doesn't belong to user.
    """
    resume = session.get(Resume, UUID(resume_id))
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if str(resume.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume"
        )
    
    return resume


@router.patch("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume_update: ResumeUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Update resume metadata (name, notes, tags).
    
    Note: This does NOT update the PDF or .tex files.
    To change files, delete and re-upload the resume.
    """
    resume = session.get(Resume, UUID(resume_id))
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if str(resume.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resume"
        )
    
    # Update only provided fields
    update_data = resume_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resume, key, value)
    
    # Update timestamp
    from datetime import datetime
    resume.updated_at = datetime.utcnow()
    
    session.add(resume)
    session.commit()
    session.refresh(resume)
    
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Delete a resume and its associated files from storage.
    
    This action cannot be undone.
    """
    resume = session.get(Resume, UUID(resume_id))
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if str(resume.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resume"
        )
    
    # Delete files from storage
    await delete_file(resume.pdf_url)
    if resume.tex_url:
        await delete_file(resume.tex_url)
    
    # Delete database record
    session.delete(resume)
    session.commit()
    
    return None


@router.post("/{resume_id}/clone", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def clone_resume(
    resume_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Clone an existing resume (creates a copy with " (Copy)" appended to name).
    
    The cloned resume references the same files (no re-upload needed).
    This is useful for creating variations from existing versions.
    """
    original = session.get(Resume, UUID(resume_id))
    
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if str(original.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to clone this resume"
        )
    
    # Create clone
    clone = Resume(
        user_id=UUID(user_id),
        name=f"{original.name} (Copy)",
        notes=original.notes,
        pdf_url=original.pdf_url,
        tex_url=original.tex_url,
        tags=original.tags.copy() if original.tags else None
    )
    
    session.add(clone)
    session.commit()
    session.refresh(clone)
    
    return clone
