from supabase import create_client, Client
from app.config import settings
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException


# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Storage bucket name
RESUME_BUCKET = "resumes"


async def upload_file(
    file: UploadFile,
    user_id: str,
    file_type: str
) -> str:
    """
    Upload file to Supabase Storage and return public URL.
    
    Args:
        file: The uploaded file (PDF or .tex)
        user_id: User's UUID for scoped storage path
        file_type: 'pdf' or 'tex'
        
    Returns:
        Public URL of the uploaded file
        
    Raises:
        HTTPException: If upload fails
    """
    try:
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else file_type
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        storage_path = f"{user_id}/{unique_filename}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(RESUME_BUCKET).upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": file.content_type or f"application/{file_type}"}
        )
        
        # Get public URL
        public_url = supabase.storage.from_(RESUME_BUCKET).get_public_url(storage_path)
        
        return public_url
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )


async def delete_file(file_url: str) -> None:
    """
    Delete file from Supabase Storage.
    
    Args:
        file_url: Public URL of the file to delete
        
    Raises:
        HTTPException: If deletion fails
    """
    try:
        # Extract storage path from URL
        # Format: https://xxx.supabase.co/storage/v1/object/public/resumes/{path}
        if "/resumes/" not in file_url:
            return  # Not a valid resume storage URL
        
        storage_path = file_url.split("/resumes/")[-1]
        
        # Delete from Supabase Storage
        supabase.storage.from_(RESUME_BUCKET).remove([storage_path])
        
    except Exception as e:
        # Log error but don't fail the request if file doesn't exist
        print(f"File deletion warning: {str(e)}")


async def get_file_url(storage_path: str) -> str:
    """
    Get public URL for a file in storage.
    
    Args:
        storage_path: Path in storage bucket
        
    Returns:
        Public URL of the file
    """
    return supabase.storage.from_(RESUME_BUCKET).get_public_url(storage_path)


async def validate_file_size(file: UploadFile, max_size_mb: int = 5) -> None:
    """
    Validate file size before upload.
    
    Args:
        file: The uploaded file
        max_size_mb: Maximum allowed size in MB
        
    Raises:
        HTTPException: If file is too large
    """
    # Read file to get size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    
    # Reset file position for subsequent reads
    await file.seek(0)
    
    if size_mb > max_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {max_size_mb}MB, got {size_mb:.2f}MB"
        )


async def validate_file_type(file: UploadFile, allowed_types: list) -> None:
    """
    Validate file type/extension.
    
    Args:
        file: The uploaded file
        allowed_types: List of allowed extensions (e.g., ['pdf', 'tex'])
        
    Raises:
        HTTPException: If file type is not allowed
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type .{file_extension} not allowed. Allowed types: {', '.join(allowed_types)}"
        )
