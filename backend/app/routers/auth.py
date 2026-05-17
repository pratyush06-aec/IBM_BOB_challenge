"""
Authentication Router - Firebase Integration
Handles user authentication using Firebase
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel

from ..firebase_service import FirebaseService, FirebaseUser

router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


class TokenResponse(BaseModel):
    """Token response model"""
    message: str
    user: dict


class UserResponse(BaseModel):
    """User response model"""
    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    email_verified: bool = False


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> FirebaseUser:
    """
    Dependency to get current authenticated user from Firebase token
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        FirebaseUser object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    user = FirebaseService.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/verify", response_model=TokenResponse)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify Firebase ID token
    
    This endpoint verifies the Firebase ID token sent from the client.
    The actual sign-in/sign-up happens on the client side using Firebase Auth.
    
    Returns:
        Token verification response with user info
    """
    user = await get_current_user(credentials)
    
    return TokenResponse(
        message="Token verified successfully",
        user={
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "email_verified": user.email_verified
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: FirebaseUser = Depends(get_current_user)):
    """
    Get current user information
    
    Returns:
        Current user details
    """
    return UserResponse(
        uid=current_user.uid,
        email=current_user.email,
        display_name=current_user.display_name,
        email_verified=current_user.email_verified
    )


@router.post("/logout")
async def logout():
    """
    Logout endpoint
    
    Note: With Firebase, logout is handled on the client side.
    This endpoint is provided for API consistency.
    
    Returns:
        Logout confirmation message
    """
    return {"message": "Logout successful. Clear token on client side."}


# Health check for auth service
@router.get("/health")
async def auth_health():
    """
    Check if Firebase authentication is properly configured
    
    Returns:
        Health status of auth service
    """
    is_initialized = FirebaseService._initialized
    
    return {
        "status": "healthy" if is_initialized else "degraded",
        "firebase_initialized": is_initialized,
        "message": "Firebase authentication is ready" if is_initialized else "Firebase not configured"
    }

# Made with Bob
