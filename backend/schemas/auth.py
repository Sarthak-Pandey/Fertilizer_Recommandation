"""
Authentication schemas for request validation and response serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Schema for user registration request."""
    email: EmailStr = Field(..., description="User valid email address")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    role: Optional[str] = Field("farmer", description="User role: farmer | agronomist | admin")
    organization: Optional[str] = Field(None, description="Organization or farm name")


class UserLoginRequest(BaseModel):
    """Schema for user login credentials."""
    email: EmailStr = Field(..., description="User registered email address")
    password: str = Field(..., description="User password")


class UserProfileResponse(BaseModel):
    """User profile data structure."""
    id: str = Field(..., description="Unique UUID identifier from Supabase Auth")
    email: str = Field(..., description="Registered email address")
    full_name: Optional[str] = None
    role: Optional[str] = "farmer"
    organization: Optional[str] = None
    created_at: Optional[str] = None


class AuthTokenResponse(BaseModel):
    """Response returned upon successful authentication containing JWT tokens."""
    access_token: str = Field(..., description="JWT access token for Authorization header")
    refresh_token: Optional[str] = Field(None, description="Refresh token for extending session")
    token_type: str = Field("bearer", description="Token type, always 'bearer'")
    user: UserProfileResponse = Field(..., description="User profile metadata")
