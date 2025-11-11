from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Note: Supabase handles authentication, this endpoint just verifies
    the JWT token and returns the user_id.
    """
    return {"user_id": user_id, "message": "Authentication successful"}
