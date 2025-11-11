from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_, and_, col
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime

from app.database import get_session
from app.auth.dependencies import get_current_user
from app.applications.models import (
    Application,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithResume,
    StatusEnum
)
from app.resumes.models import Resume

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Create a new job application.
    
    - **company**: Company name (required)
    - **role**: Job role/title (required)
    - **date_applied**: Date of application (required)
    - **status**: Current status (default: "applied")
    - **notes**: Optional notes
    - **resume_id**: ID of resume used (optional, links to resume)
    - **follow_up_date**: Date to follow up (optional)
    """
    # Validate resume_id if provided
    if application.resume_id:
        resume = session.get(Resume, application.resume_id)
        if not resume or str(resume.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or doesn't belong to user"
            )
    
    # Create application
    db_application = Application(
        **application.dict(),
        user_id=UUID(user_id)
    )
    
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    
    return db_application


@router.post("/quick", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def quick_add_application(
    company: str,
    role: str,
    resume_id: Optional[str] = None,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Quick add application with minimal fields (for bulk apply sessions).
    
    - **company**: Company name (required)
    - **role**: Job role (required)
    - **resume_id**: Resume used (optional)
    
    Auto-sets:
    - date_applied: Today
    - status: "applied"
    """
    # Validate resume_id if provided
    resume_uuid = None
    if resume_id:
        resume = session.get(Resume, UUID(resume_id))
        if not resume or str(resume.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        resume_uuid = UUID(resume_id)
    
    # Create application with defaults
    application = Application(
        user_id=UUID(user_id),
        company=company,
        role=role,
        date_applied=date.today(),
        status=StatusEnum.applied,
        resume_id=resume_uuid
    )
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    return application


@router.get("/", response_model=List[ApplicationWithResume])
async def list_applications(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search company or role"),
    resume_id: Optional[str] = Query(None, description="Filter by resume ID"),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    List all applications for the authenticated user.
    
    Supports:
    - **status**: Filter by status (applied, interview, offer, rejected, archived)
    - **search**: Search in company name or role
    - **resume_id**: Filter by resume used
    
    Returns applications ordered by date_applied (newest first).
    Includes resume name if application is linked to a resume.
    """
    # Base query
    statement = select(Application).where(
        Application.user_id == UUID(user_id)
    )
    
    # Apply status filter
    if status_filter:
        try:
            status_enum = StatusEnum(status_filter.lower())
            statement = statement.where(Application.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}. Must be one of: {', '.join([s.value for s in StatusEnum])}"
            )
    
    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            or_(
                col(Application.company).ilike(search_pattern),
                col(Application.role).ilike(search_pattern)
            )
        )
    
    # Apply resume filter
    if resume_id:
        statement = statement.where(Application.resume_id == UUID(resume_id))
    
    # Order by date
    statement = statement.order_by(Application.date_applied.desc())
    
    # Execute query
    applications = session.exec(statement).all()
    
    # Enrich with resume names
    result = []
    for app in applications:
        app_dict = app.dict()
        
        # Get resume name if linked
        if app.resume_id:
            resume = session.get(Resume, app.resume_id)
            app_dict['resume_name'] = resume.name if resume else None
        else:
            app_dict['resume_name'] = None
        
        result.append(ApplicationWithResume(**app_dict))
    
    return result


@router.get("/{application_id}", response_model=ApplicationWithResume)
async def get_application(
    application_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get a specific application by ID.
    
    Returns 404 if application doesn't exist or doesn't belong to user.
    Includes resume name if application is linked.
    """
    application = session.get(Application, UUID(application_id))
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if str(application.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application"
        )
    
    # Enrich with resume name
    app_dict = application.dict()
    if application.resume_id:
        resume = session.get(Resume, application.resume_id)
        app_dict['resume_name'] = resume.name if resume else None
    else:
        app_dict['resume_name'] = None
    
    return ApplicationWithResume(**app_dict)


@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: str,
    application_update: ApplicationUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Update an application's fields.
    
    All fields are optional - only provided fields will be updated.
    Automatically updates last_updated timestamp.
    """
    application = session.get(Application, UUID(application_id))
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if str(application.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    # Validate resume_id if being updated
    update_data = application_update.dict(exclude_unset=True)
    if 'resume_id' in update_data and update_data['resume_id']:
        resume = session.get(Resume, update_data['resume_id'])
        if not resume or str(resume.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
    
    # Update fields
    for key, value in update_data.items():
        setattr(application, key, value)
    
    # Update timestamp
    application.last_updated = datetime.utcnow()
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Delete an application.
    
    This action cannot be undone.
    Note: This does NOT delete the linked resume, only the application record.
    """
    application = session.get(Application, UUID(application_id))
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if str(application.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this application"
        )
    
    session.delete(application)
    session.commit()
    
    return None


@router.get("/stats/summary")
async def get_application_stats(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get application statistics for the user.
    
    Returns:
    - Total applications
    - Count by status
    - Upcoming follow-ups
    """
    # Get all applications
    statement = select(Application).where(Application.user_id == UUID(user_id))
    applications = session.exec(statement).all()
    
    # Calculate stats
    total = len(applications)
    by_status = {}
    for status in StatusEnum:
        by_status[status.value] = len([a for a in applications if a.status == status])
    
    # Upcoming follow-ups
    today = date.today()
    upcoming_followups = [
        {
            "id": str(a.id),
            "company": a.company,
            "role": a.role,
            "follow_up_date": a.follow_up_date.isoformat()
        }
        for a in applications
        if a.follow_up_date and a.follow_up_date >= today and a.status not in [StatusEnum.rejected, StatusEnum.archived]
    ]
    upcoming_followups.sort(key=lambda x: x['follow_up_date'])
    
    return {
        "total_applications": total,
        "by_status": by_status,
        "upcoming_followups": upcoming_followups[:5]  # Next 5
    }
