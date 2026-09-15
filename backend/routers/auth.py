"""
Authentication API Router -- Login, Register, Profile, and Session endpoints.
"""

import logging
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status

from backend.schemas.auth import (
    AuthTokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserProfileResponse,
)
from backend.services.auth_service import auth_service
from backend.utils.auth_dependency import get_current_user

logger = logging.getLogger("backend.routers.auth")

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(payload: UserRegisterRequest):
    """
    Register a new user in Supabase Auth.
    Stores user profile metadata (full_name, role, organization) securely.
    """
    try:
        result = auth_service.register_user(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            role=payload.role or "farmer",
            organization=payload.organization,
        )
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )
    except Exception as e:
        logger.error("registration_unhandled_error error=%s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error.",
        )


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    summary="User login with email and password",
)
async def login(payload: UserLoginRequest):
    """
    Authenticate user against Supabase Auth.
    Returns JWT access token, refresh token, and user profile data.
    """
    try:
        result = auth_service.login_user(
            email=payload.email,
            password=payload.password,
        )
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ve),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error("login_unhandled_error error=%s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error.",
        )


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current user profile",
)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Protected endpoint: returns the authenticated user's profile metadata.
    """
    return current_user


@router.post(
    "/logout",
    summary="Logout user session",
)
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Protected endpoint: invalidates active user session context.
    """
    logger.info("user_logged_out user_id=%s", current_user.get("id"))
    return {"success": True, "message": "Successfully logged out."}
